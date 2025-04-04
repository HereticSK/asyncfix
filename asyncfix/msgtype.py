"""Message type module."""
import enum


class _MsgTypeEnumMeta(enum.EnumMeta):
    def __contains__(cls, item):
        if isinstance(item, enum.Enum):
            return isinstance(item, cls) and item._name_ in cls._member_map_
        else:
            return item in cls._value2member_map_


class FMsg(enum.Enum, metaclass=_MsgTypeEnumMeta):
    """FIXMessage type enum."""

    def __str__(self):
        """To string."""
        return str(self.value)

    def __eq__(self, o):
        """Equality check."""
        return self.value == o

    def __hash__(self):
        """Hash by value."""
        return hash(self.value)

    HEARTBEAT = "0"
    TESTREQUEST = "1"
    RESENDREQUEST = "2"
    REJECT = "3"
    SEQUENCERESET = "4"
    LOGOUT = "5"
    IOI = "6"
    ADVERTISEMENT = "7"
    EXECUTIONREPORT = "8"
    ORDERCANCELREJECT = "9"
    QUOTESTATUSREQUEST = "a"
    LOGON = "A"
    DERIVATIVESECURITYLIST = "AA"
    NEWORDERMULTILEG = "AB"
    MULTILEGORDERCANCELREPLACE = "AC"
    TRADECAPTUREREPORTREQUEST = "AD"
    TRADECAPTUREREPORT = "AE"
    ORDERMASSSTATUSREQUEST = "AF"
    QUOTEREQUESTREJECT = "AG"
    RFQREQUEST = "AH"
    QUOTESTATUSREPORT = "AI"
    QUOTERESPONSE = "AJ"
    CONFIRMATION = "AK"
    POSITIONMAINTENANCEREQUEST = "AL"
    POSITIONMAINTENANCEREPORT = "AM"
    REQUESTFORPOSITIONS = "AN"
    REQUESTFORPOSITIONSACK = "AO"
    POSITIONREPORT = "AP"
    TRADECAPTUREREPORTREQUESTACK = "AQ"
    TRADECAPTUREREPORTACK = "AR"
    ALLOCATIONREPORT = "AS"
    ALLOCATIONREPORTACK = "AT"
    CONFIRMATIONACK = "AU"
    SETTLEMENTINSTRUCTIONREQUEST = "AV"
    ASSIGNMENTREPORT = "AW"
    COLLATERALREQUEST = "AX"
    COLLATERALASSIGNMENT = "AY"
    COLLATERALRESPONSE = "AZ"
    NEWS = "B"
    MASSQUOTEACKNOWLEDGEMENT = "b"
    COLLATERALREPORT = "BA"
    COLLATERALINQUIRY = "BB"
    NETWORKCOUNTERPARTYSYSTEMSTATUSREQUEST = "BC"
    NETWORKCOUNTERPARTYSYSTEMSTATUSRESPONSE = "BD"
    USERREQUEST = "BE"
    USERRESPONSE = "BF"
    COLLATERALINQUIRYACK = "BG"
    CONFIRMATIONREQUEST = "BH"
    EMAIL = "C"
    SECURITYDEFINITIONREQUEST = "c"
    SECURITYDEFINITION = "d"
    NEWORDERSINGLE = "D"
    SECURITYSTATUSREQUEST = "e"
    NEWORDERLIST = "E"
    ORDERCANCELREQUEST = "F"
    SECURITYSTATUS = "f"
    ORDERCANCELREPLACEREQUEST = "G"
    TRADINGSESSIONSTATUSREQUEST = "g"
    ORDERSTATUSREQUEST = "H"
    TRADINGSESSIONSTATUS = "h"
    MASSQUOTE = "i"
    BUSINESSMESSAGEREJECT = "j"
    ALLOCATIONINSTRUCTION = "J"
    BIDREQUEST = "k"
    LISTCANCELREQUEST = "K"
    BIDRESPONSE = "l"
    LISTEXECUTE = "L"
    LISTSTRIKEPRICE = "m"
    LISTSTATUSREQUEST = "M"
    XMLNONFIX = "n"
    LISTSTATUS = "N"
    REGISTRATIONINSTRUCTIONS = "o"
    REGISTRATIONINSTRUCTIONSRESPONSE = "p"
    ALLOCATIONINSTRUCTIONACK = "P"
    ORDERMASSCANCELREQUEST = "q"
    DONTKNOWTRADEDK = "Q"
    QUOTEREQUEST = "R"
    ORDERMASSCANCELREPORT = "r"
    QUOTE = "S"
    NEWORDERCROSS = "s"
    SETTLEMENTINSTRUCTIONS = "T"
    CROSSORDERCANCELREPLACEREQUEST = "t"
    CROSSORDERCANCELREQUEST = "u"
    MARKETDATAREQUEST = "V"
    SECURITYTYPEREQUEST = "v"
    SECURITYTYPES = "w"
    MARKETDATASNAPSHOTFULLREFRESH = "W"
    SECURITYLISTREQUEST = "x"
    MARKETDATAINCREMENTALREFRESH = "X"
    MARKETDATAREQUESTREJECT = "Y"
    SECURITYLIST = "y"
    QUOTECANCEL = "Z"
    DERIVATIVESECURITYLISTREQUEST = "z"