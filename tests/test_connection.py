import logging
import asyncio
import os
import warnings
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock

import pytest
import pytest_asyncio

from asyncfix import FIXMessage, FMsg, FTag
from asyncfix.connection import AsyncFIXConnection, ConnectionRole, ConnectionState
from asyncfix.errors import FIXConnectionError
from asyncfix.journaler import Journaler
from asyncfix.message import MessageDirection
from asyncfix.protocol import FIXProtocol44, FIXSchema
from asyncfix.protocol.fix_tester import FIXTester
from asyncfix.protocol.order_single import FIXNewOrderSingle

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
fix44_schema = ET.parse(os.path.join(TEST_DIR, "FIX44.xml"))
FIX_SCHEMA = FIXSchema(fix44_schema)


@pytest_asyncio.fixture
async def fix_connection():
    log = logging.getLogger("asyncfix_test")
    log.setLevel(logging.DEBUG)
    j = Journaler()
    connection = AsyncFIXConnection(
        FIXProtocol44(),
        "INITIATOR",
        "ACCEPTOR",
        journaler=j,
        host="localhost",
        port="64444",
        heartbeat_period=30,
        start_tasks=False,
        logger=log,
    )
    connection._connection_state = ConnectionState.NETWORK_CONN_ESTABLISHED
    assert connection._connection_role == ConnectionRole.UNKNOWN
    return connection


@pytest.mark.asyncio
async def test_connection_send_not_connected_error(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)
    msg = ft.msg_logon()

    for state in [
        ConnectionState.DISCONNECTED_NOCONN_TODAY,
        ConnectionState.DISCONNECTED_BROKEN_CONN,
        ConnectionState.DISCONNECTED_WCONN_TODAY,
        ConnectionState.AWAITING_CONNECTION,
        ConnectionState.INITIATE_CONNECTION,
    ]:
        conn._connection_state = state
        with pytest.raises(
            FIXConnectionError,
            match="Connection must be established before sending any FIX message",
        ):
            await conn.send_msg(msg)


@pytest.mark.asyncio
async def test_connection_send_first_logon_sets_state(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._connection_state = ConnectionState.NETWORK_CONN_ESTABLISHED
    msg = ft.msg_logon()
    await conn.send_msg(msg)
    assert conn._connection_state == ConnectionState.LOGON_INITIAL_SENT

    # This is not allowed until logon confirmation!
    with pytest.raises(
        FIXConnectionError,
        match=(
            r"Initiator is waiting for Logon\(\) response, you must not send any"
            r" additional messages before"
        ),
    ):
        await conn.send_msg(ft.msg_heartbeat())


@pytest.mark.asyncio
async def test_connection_send_first_must_be_logon(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._connection_state = ConnectionState.NETWORK_CONN_ESTABLISHED
    msg = ft.msg_sequence_reset(1, 12)
    with pytest.raises(
        FIXConnectionError,
        match=(
            r"You must send first Logon\(35=A\)/Logout\(\) message immediately after"
            r" connection.*"
        ),
    ):
        await conn.send_msg(msg)

    assert conn.connection_state == ConnectionState.NETWORK_CONN_ESTABLISHED


@pytest.mark.asyncio
async def test_connection_logon_acceptor_logon(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    assert conn._connection_state == ConnectionState.NETWORK_CONN_ESTABLISHED
    rmsg = await ft.reply(ft.msg_logon())
    assert conn.connection_role == ConnectionRole.ACCEPTOR
    assert conn._connection_state == ConnectionState.ACTIVE


@pytest.mark.asyncio
async def test_connection_logon_acceptor_logon_first_message_expected(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    assert conn._connection_state == ConnectionState.NETWORK_CONN_ESTABLISHED
    msg_reset = ft.msg_sequence_reset(1, 2)
    rmsg = await ft.reply(msg_reset)
    assert conn._connection_state == ConnectionState.DISCONNECTED_BROKEN_CONN


@pytest.mark.asyncio
async def test_connection_logon_valid(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    assert conn._connection_role == ConnectionRole.INITIATOR
    assert conn._connection_state == ConnectionState.LOGON_INITIAL_SENT

    assert len(ft.initiator_sent) == 1

    assert ft.initiator_sent_query((FTag.SenderCompID, FTag.TargetCompID)) == {
        FTag.SenderCompID: "INITIATOR",
        FTag.TargetCompID: "ACCEPTOR",
    }

    assert ft.initiator_sent_query((35, 34)) == {FTag.MsgType: FMsg.LOGON, "34": "1"}

    rmsg = await ft.reply(ft.msg_logon())
    assert conn._connection_state == ConnectionState.ACTIVE
    # FIX Tester.reply() - simulated server response (SenderCompID/TargetCompID swapped)
    assert rmsg.query(FTag.SenderCompID, FTag.TargetCompID) == {
        FTag.TargetCompID: "INITIATOR",
        FTag.SenderCompID: "ACCEPTOR",
    }


@pytest.mark.asyncio
async def test_connection_logon_low_seq_num_by_initator(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._session.next_num_out = 20
    ft.set_next_num(num_in=21)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    assert conn._connection_role == ConnectionRole.INITIATOR
    assert conn._connection_state == ConnectionState.LOGON_INITIAL_SENT

    assert len(ft.initiator_sent) == 1

    assert ft.initiator_sent_query((FTag.SenderCompID, FTag.TargetCompID)) == {
        FTag.SenderCompID: "INITIATOR",
        FTag.TargetCompID: "ACCEPTOR",
    }

    assert ft.initiator_sent_query((35, 34)) == {FTag.MsgType: FMsg.LOGON, "34": "20"}

    await ft.process_msg_acceptor()

    assert ft.conn_accept._connection_state == ConnectionState.DISCONNECTED_BROKEN_CONN
    assert conn._connection_state == ConnectionState.DISCONNECTED_BROKEN_CONN

    assert ft.acceptor_sent_query((35, 58)) == {
        FTag.MsgType: FMsg.LOGOUT,
        "58": "MsgSeqNum is too low, expected 21, got 20",
    }


@pytest.mark.asyncio
async def test_connection_logon_low_seq_num_by_acceptor(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    assert conn._connection_role == ConnectionRole.INITIATOR
    assert conn._connection_state == ConnectionState.LOGON_INITIAL_SENT

    assert len(ft.initiator_sent) == 1

    assert ft.initiator_sent_query((FTag.SenderCompID, FTag.TargetCompID)) == {
        FTag.SenderCompID: "INITIATOR",
        FTag.TargetCompID: "ACCEPTOR",
    }

    assert ft.initiator_sent_query((35, 34)) == {FTag.MsgType: FMsg.LOGON, "34": "1"}

    conn._session.next_num_in = 10
    ft.set_next_num(num_out=4)
    await ft.process_msg_acceptor()
    assert len(ft.initiator_sent) == 2
    assert len(ft.acceptor_sent) == 2
    assert ft.acceptor_sent_query((35, 34), 0) == {FTag.MsgType: FMsg.LOGON, "34": "4"}
    assert ft.acceptor_sent_query((35, 34), 1) == {
        FTag.MsgType: FMsg.TESTREQUEST,
        "34": "5",
    }
    assert ft.initiator_sent_query((35, 58)) == {
        FTag.MsgType: FMsg.LOGOUT,
        "58": "MsgSeqNum is too low, expected 10, got 4",
    }

    assert ft.conn_accept._connection_state == ConnectionState.DISCONNECTED_WCONN_TODAY
    assert conn._connection_state == ConnectionState.DISCONNECTED_BROKEN_CONN


@pytest.mark.asyncio
async def test_connection_validation_missing_seqnum(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    msg_out = ft.initiator_sent[-1]

    del msg_out[34]
    assert ft.conn_accept._validate_integrity(msg_out) == "MsgSeqNum(34) tag is missing"


@pytest.mark.asyncio
async def test_connection_validation_seqnum_toolow(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._session.next_num_out = 20

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    msg_out = ft.initiator_sent[-1]
    ft.set_next_num(num_in=21)

    assert (
        ft.conn_accept._validate_integrity(msg_out)
        == "MsgSeqNum is too low, expected 21, got 20"
    )


@pytest.mark.asyncio
async def test_connection_validation_beginstring(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    msg_out = ft.initiator_sent[-1]
    msg_out.set(FTag.BeginString, "FIX4.8", replace=True)

    assert (
        ft.conn_accept._validate_integrity(msg_out)
        == "Protocol BeginString(8) mismatch, expected FIX.4.4, got FIX4.8"
    )


@pytest.mark.asyncio
async def test_connection_validation_no_target(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    msg_out = ft.initiator_sent[-1]
    del msg_out[FTag.TargetCompID]

    assert conn._validate_integrity(msg_out) is True


@pytest.mark.asyncio
async def test_connection_validation_no_sender(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    msg_out = ft.initiator_sent[-1]
    del msg_out[FTag.SenderCompID]

    assert conn._validate_integrity(msg_out) is True


@pytest.mark.asyncio
async def test_connection_validation_sender_mismatch(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    msg_out = ft.initiator_sent[-1]
    msg_out.set(FTag.SenderCompID, "as", replace=True)

    assert conn._validate_integrity(msg_out) == "TargetCompID / SenderCompID mismatch"


@pytest.mark.asyncio
async def test_connection_validation_target_mismatch(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    msg_out = ft.initiator_sent[-1]
    msg_out.set(FTag.TargetCompID, "as", replace=True)

    assert conn._validate_integrity(msg_out) == "TargetCompID / SenderCompID mismatch"


@pytest.mark.asyncio
async def test_connection__process_resend_req_synth(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    with patch.object(conn, "_journaler") as mock__journaler:
        msgs = [
            FIXMessage(FMsg.LOGON),
            FIXMessage(FMsg.HEARTBEAT),
            FIXNewOrderSingle("test", "ticker", "1", 10, 10).new_req(),
            FIXMessage(FMsg.HEARTBEAT),
            FIXMessage(FMsg.TESTREQUEST),
            FIXMessage(FMsg.RESENDREQUEST),
            FIXMessage(FMsg.SEQUENCERESET, {FTag.NewSeqNo: 800}),
            FIXNewOrderSingle("test", "ticker", "1", 10, 10).new_req(),
            FIXMessage(FMsg.TESTREQUEST),
        ]
        seq_res = msgs[6]
        assert seq_res.msg_type == FMsg.SEQUENCERESET
        seq_res[34] = conn._session.next_num_out + 5
        assert seq_res[34] == "6"
        enc_msg = [conn._codec.encode(m, conn._session).encode() for m in msgs]
        mock__journaler.recover_messages.return_value = enc_msg

        conn._session.next_num_out = 20

        resend_req = FIXMessage(
            FMsg.RESENDREQUEST,
            {FTag.BeginSeqNo: 1, FTag.EndSeqNo: "0"},
        )
        conn._connection_state = ConnectionState.RESENDREQ_HANDLING
        await conn._process_resend(resend_req)
        conn._connection_state = ConnectionState.ACTIVE

        assert len(ft.initiator_sent) == 5
        assert ft.initiator_sent[0].query(35, 34, 36, 123) == {
            FTag.MsgType: str(FMsg.SEQUENCERESET),
            FTag.MsgSeqNum: "1",
            FTag.NewSeqNo: "3",
            FTag.GapFillFlag: "Y",
        }

        assert ft.initiator_sent[1].query(35, 34, FTag.PossDupFlag) == {
            FTag.MsgType: str(FMsg.NEWORDERSINGLE),
            FTag.MsgSeqNum: "3",
            FTag.PossDupFlag: "Y",
        }

        assert ft.initiator_sent[2].query(35, 34, 36, 123) == {
            FTag.MsgType: str(FMsg.SEQUENCERESET),
            FTag.MsgSeqNum: "4",
            FTag.NewSeqNo: "7",
            FTag.GapFillFlag: "Y",
        }

        assert ft.initiator_sent[3].query(35, 34, FTag.PossDupFlag) == {
            FTag.MsgType: str(FMsg.NEWORDERSINGLE),
            FTag.MsgSeqNum: "7",
            FTag.PossDupFlag: "Y",
        }

        assert ft.initiator_sent[4].query(35, 34, 36, 123) == {
            FTag.MsgType: str(FMsg.SEQUENCERESET),
            FTag.MsgSeqNum: "8",
            FTag.NewSeqNo: "20",
            FTag.GapFillFlag: "Y",
        }


@pytest.mark.asyncio
async def test_sequence_reset_request__no_gap(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()

    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE

    seqreset_msg = FIXMessage(
        FMsg.SEQUENCERESET,
        {FTag.NewSeqNo: 10, FTag.MsgSeqNum: conn._session.next_num_out},
    )
    await conn.send_msg(seqreset_msg)
    await ft.process_msg_acceptor()

    assert ft.conn_accept._session.next_num_in == 10


@pytest.mark.asyncio
async def test_sequence_reset_request__unexpected_gapfillflag(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()

    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE

    seqreset_msg = FIXMessage(
        FMsg.SEQUENCERESET,
        {
            FTag.NewSeqNo: 10,
            FTag.MsgSeqNum: conn._session.next_num_out,
            FTag.GapFillFlag: "Y",
        },
    )
    await conn.send_msg(seqreset_msg)
    await ft.process_msg_acceptor()

    assert ft.conn_accept._session.next_num_in == 10


@pytest.mark.asyncio
async def test__finalize_message(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_sequence_reset(1, 10, is_gap_fill=True)
    assert conn._message_last_time == 0

    with patch.object(conn, "_journaler") as mock_journaler:
        await conn._finalize_message(msg, b"msg")
        assert conn._message_last_time > 0
        assert mock_journaler.persist_msg.called
        assert mock_journaler.persist_msg.call_args[0] == (
            b"msg",
            conn._session,
            MessageDirection.INBOUND,
        )
        assert mock_journaler.persist_msg.call_args[1] == {}
        assert conn._session.next_num_in == 10

    msg = ft.msg_sequence_reset(10, 15, is_gap_fill=True)
    del msg[FTag.NewSeqNo]
    assert conn._session.set_next_num_in(msg) == 0

    with patch.object(conn, "_journaler") as mock_journaler:
        await conn._finalize_message(msg, b"msg")
        assert not mock_journaler.persist_msg.called
        assert conn._session.next_num_in == 10

    msg = ft.msg_logon()
    assert FTag.MsgSeqNum not in msg
    assert conn._session.set_next_num_in(msg) == 0

    with patch.object(conn, "_journaler") as mock_journaler:
        await conn._finalize_message(msg, b"msg")
        assert not mock_journaler.persist_msg.called
        assert conn._session.next_num_in == 10

    msg = ft.msg_logon()
    msg[FTag.MsgSeqNum] = 100
    assert conn._session.set_next_num_in(msg) == -1

    with patch.object(conn, "_journaler") as mock_journaler:
        await conn._finalize_message(msg, b"msg")
        assert not mock_journaler.persist_msg.called
        assert conn._session.next_num_in == 10


@pytest.mark.asyncio
async def test_connection_both_seqnum_mismach_bidirectional_resend_req(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._session.next_num_out = 20
    conn._session.next_num_in = 25
    ft.set_next_num(num_in=15, num_out=30)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE

    conn.log.debug(100 * "-")
    conn._session.next_num_out = 40
    await conn.send_msg(ft.msg_heartbeat())
    await ft.process_msg_acceptor()
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE


@pytest.mark.asyncio
async def test_test_request_exchange(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE

    await conn.send_test_req()
    await ft.process_msg_acceptor()

    assert conn._test_req_id is None
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE


@pytest.mark.asyncio
async def test_test_incorrect_response(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE

    with patch.object(ft.conn_accept, "_process_testrequest") as mock__process_testreq:

        async def _mock_test_req(msg):
            m = ft.msg_heartbeat("asd")
            await ft.conn_accept.send_msg(m)

        mock__process_testreq.side_effect = _mock_test_req

        await conn.send_test_req()
        await ft.process_msg_acceptor()

        assert conn._test_req_id is None
        assert (
            ft.conn_accept._connection_state == ConnectionState.DISCONNECTED_WCONN_TODAY
        )
        assert (
            ft.conn_init._connection_state == ConnectionState.DISCONNECTED_BROKEN_CONN
        )


@pytest.mark.asyncio
async def test_test_request_errors_side_cases(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE

    with pytest.raises(
        FIXConnectionError,
        match=r"You must rend TestRequest\(\) message via self.send_test_req",
    ):
        testmsg = ft.msg_test_request("123")
        await conn.send_msg(testmsg)

    with patch.object(ft.conn_accept, "_process_testrequest") as mock__process_testreq:

        async def _mock_test_req(msg):
            m = ft.msg_heartbeat()
            await ft.conn_accept.send_msg(m)

        mock__process_testreq.side_effect = _mock_test_req

        await conn.send_test_req()
        await ft.process_msg_acceptor()

        with pytest.raises(
            FIXConnectionError, match=r"Another test request already pending"
        ):
            await conn.send_test_req()

        # No Heartbeat(TestReqId) given, just skip until we get valid one
        assert conn._test_req_id is not None
        assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
        assert ft.conn_init._connection_state == ConnectionState.ACTIVE


@pytest.mark.asyncio
async def test_extra_msg_during_seq_num_resend_alredy_journaled(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._session.next_num_out = 20
    conn._session.next_num_in = 25
    ft.set_next_num(num_in=15, num_out=30)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE

    conn.log.debug(100 * "-")

    # replace INITIATOR Journaler to avoid duplicate SQL error (just mock)
    conn._journaler = Journaler()
    conn._session.next_num_out = 15

    ord = FIXNewOrderSingle("test", "ticker", "1", 10, 10).new_req()
    ord[FTag.MsgSeqNum] = 15
    ord[FTag.PossDupFlag] = "Y"

    await conn.send_msg(ord)
    await ft.process_msg_acceptor()

    assert ft.conn_init._connection_state == ConnectionState.DISCONNECTED_WCONN_TODAY
    assert ft.conn_accept._connection_state == ConnectionState.DISCONNECTED_BROKEN_CONN


@pytest.mark.asyncio
async def test_extra_msg_during_seq_num_resend_low_num_not_processed(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._session.next_num_out = 20
    conn._session.next_num_in = 25
    ft.set_next_num(num_in=15, num_out=30)

    msg = ft.msg_logon()
    await conn.send_msg(msg)
    await ft.process_msg_acceptor()
    assert ft.conn_init._connection_state == ConnectionState.ACTIVE
    assert ft.conn_accept._connection_state == ConnectionState.ACTIVE

    conn.log.debug(100 * "-")
    # ft.set_next_num(num_in=15)
    with patch.object(ft.conn_accept, "_journaler") as mock_journaler:
        mock_journaler.persist_msg.reset_mock()
        conn._session.next_num_out = 17
        await conn.send_msg(ft.msg_heartbeat())
        await conn.send_msg(ft.msg_heartbeat())
        await ft.process_msg_acceptor()

        assert (
            ft.conn_init._connection_state == ConnectionState.DISCONNECTED_WCONN_TODAY
        )
        assert (
            ft.conn_accept._connection_state == ConnectionState.DISCONNECTED_BROKEN_CONN
        )
        assert len(mock_journaler.persist_msg.call_args_list) == 1
        assert (
            mock_journaler.persist_msg.call_args_list[0][0][2]
            == MessageDirection.OUTBOUND
        )


@pytest.mark.asyncio
async def test_connection__process_resend_req_real_processing(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    with (
        patch.object(conn, "_journaler") as mock__journaler,
        patch.object(ft.conn_accept, "on_message") as mock_on_message,
    ):
        msgs = [
            FIXMessage(FMsg.LOGON),
            FIXMessage(FMsg.HEARTBEAT),
            FIXNewOrderSingle("test", "ticker", "1", 10, 10).new_req(),
            FIXMessage(FMsg.HEARTBEAT),
            FIXMessage(FMsg.TESTREQUEST),
            FIXMessage(FMsg.RESENDREQUEST),
        ]
        enc_msg = [conn._codec.encode(m, conn._session).encode() for m in msgs]
        mock__journaler.recover_messages.return_value = enc_msg
        conn._session.next_num_out = 10
        msg = ft.msg_logon()
        await conn.send_msg(msg)
        await ft.process_msg_acceptor()
        assert ft.conn_init._connection_state == ConnectionState.ACTIVE
        assert ft.conn_accept._connection_state == ConnectionState.ACTIVE
        assert mock_on_message.called
        assert mock_on_message.call_count == 1
        (app_msg,) = mock_on_message.call_args[0]
        assert app_msg.query(35) == {FTag.MsgType: FMsg.NEWORDERSINGLE}


@pytest.mark.asyncio
async def test_connection__process_resend__ignores_high_seq_num_msg(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    conn._session.next_num_out = 10

    with (
        patch.object(conn, "_journaler") as mock__journaler,
        patch.object(ft.conn_accept, "on_message") as mock_on_message,
    ):
        msgs = [
            FIXMessage(FMsg.LOGON),
            FIXMessage(FMsg.HEARTBEAT),
            FIXNewOrderSingle("test", "ticker", "1", 10, 10).new_req(),
            FIXMessage(FMsg.HEARTBEAT),
            FIXMessage(FMsg.TESTREQUEST),
            FIXMessage(FMsg.RESENDREQUEST),
            FIXNewOrderSingle("test2", "ticker", "1", 10, 10).new_req(),
        ]
        enc_msg = [conn._codec.encode(m, conn._session).encode() for m in msgs]
        mock__journaler.recover_messages.return_value = enc_msg
        msg = ft.msg_logon()
        await conn.send_msg(msg)

        await ft.process_msg_acceptor(0)
        conn.log.debug(100 * "-")
        assert ft.conn_accept._connection_state == ConnectionState.RESENDREQ_AWAITING
        # Pretending that last order was sent via wire, and received before RESENDREQUEST
        #  we are sending already encoded message via socket mock
        dec_msg, _, _ = conn._codec.decode(enc_msg[-1])
        assert isinstance(dec_msg, FIXMessage)
        assert dec_msg[35] == FMsg.NEWORDERSINGLE

        # Prepend que to make OrderSingle arrive first
        ft.acceptor_rcv_que.insert(0, (dec_msg, enc_msg[-1]))
        await ft.process_msg_acceptor()

        assert mock_on_message.called
        assert mock_on_message.call_count == 2
        (app_msg,) = mock_on_message.call_args_list[0][0]
        assert app_msg.query(35, FTag.ClOrdID, FTag.PossDupFlag) == {
            FTag.MsgType: FMsg.NEWORDERSINGLE,
            FTag.ClOrdID: "test",
            FTag.PossDupFlag: "Y",
        }
        (app_msg,) = mock_on_message.call_args_list[1][0]
        assert app_msg.query(35, FTag.ClOrdID, FTag.PossDupFlag) == {
            FTag.MsgType: FMsg.NEWORDERSINGLE,
            FTag.ClOrdID: "test2",
            FTag.PossDupFlag: "Y",
        }


@pytest.mark.asyncio
async def test_connection_init_launch_tasks(fix_connection):
    conn: AsyncFIXConnection = fix_connection
    ft = FIXTester(schema=FIX_SCHEMA, connection=conn)

    journaler_mock = MagicMock()
    with (
        patch("asyncio.create_task") as mock_create_task,
        patch("asyncfix.connection.AsyncFIXConnection.socket_read_task") as t1,
        patch("asyncfix.connection.AsyncFIXConnection.heartbeat_timer_task") as t2,
    ):
        connection = AsyncFIXConnection(
            FIXProtocol44(),
            "INITIATOR",
            "ACCEPTOR",
            journaler=journaler_mock,
            host="localhost",
            port="64444",
            heartbeat_period=33,
            start_tasks=True,
        )

        assert connection._journaler is journaler_mock
        assert journaler_mock.create_or_load.call_args[0] == ("ACCEPTOR", "INITIATOR")
        assert journaler_mock.create_or_load.call_args[1] == {}

        assert connection._session == journaler_mock.create_or_load()
        assert connection._connection_state == ConnectionState.DISCONNECTED_NOCONN_TODAY
        assert connection.connection_role == ConnectionRole.UNKNOWN
        assert isinstance(connection._codec.protocol, FIXProtocol44)
        assert not connection._connection_was_active
        assert connection._heartbeat_period == 33
        assert connection._host == "localhost"
        assert connection._port == 64444
        assert connection._socket_reader is None
        assert connection._socket_writer is None
        assert connection._message_last_time == 0
        assert connection._max_seq_num_resend == 0
        assert not connection._msg_buffer
        assert connection._test_req_id is None

        assert mock_create_task.call_count == 2
        assert t1.called
        assert t2.called

        # This one just suppress warning about coro was not awaited
        await mock_create_task.call_args_list[0][0][0]
        await mock_create_task.call_args_list[1][0][0]


@pytest.mark.asyncio
async def test_connect_raises(fix_connection):
    conn: AsyncFIXConnection = fix_connection

    with pytest.raises(
        NotImplementedError, match=r"connect\(\) must be implemented in app class"
    ):
        await conn.connect()

    with pytest.raises(
        NotImplementedError, match=r"on_connect\(\) must be implemented in app class"
    ):
        await conn.on_connect()

    with pytest.raises(
        NotImplementedError, match=r"on_message\(\) must be implemented in app class"
    ):
        await conn.on_message(None)


@pytest.mark.asyncio
async def test_process_message_exception(fix_connection):
    conn: AsyncFIXConnection = fix_connection

    conn.log = MagicMock()
    with (
        patch.object(conn, "_validate_integrity") as mock__validate_integrity,
        patch.object(conn, "_finalize_message") as mock_finalize_message,
        patch.object(conn, "_process_logon") as mock_process_logon,
    ):
        mock__validate_integrity.side_effect = RuntimeError
        
        msg = FIXMessage(FMsg.LOGON)

        with pytest.raises(RuntimeError):
            await conn._process_message(msg, b'msg')

        mock__validate_integrity.return_value = None
        mock__validate_integrity.side_effect = None
        mock_process_logon.side_effect = RuntimeError
        await conn._process_message(msg, b'msg')
        
        # except block
        assert conn.log.exception.called

        # finally block
        #  not called because is_valid_msg_num - not passed
        assert not mock_finalize_message.called
        
        mock_process_logon.side_effect = asyncio.CancelledError
        with pytest.raises(asyncio.CancelledError):
            await conn._process_message(msg, b'msg')
