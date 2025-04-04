"""FIX Tags collection module."""
import enum


class _TagEnumMeta(enum.EnumMeta):
    def __contains__(cls, item):
        if isinstance(item, enum.Enum):
            return isinstance(item, cls) and item._name_ in cls._member_map_
        else:
            v = str(item)
            return v in cls._value2member_map_


class FTag(str, enum.Enum, metaclass=_TagEnumMeta):
    """All tags enum."""

    def __str__(self):
        """Convert to string."""
        return str(self.value)

    def __eq__(self, o):
        """Equality check."""
        return self.value == str(o)

    def __hash__(self):
        """Hash by tag value."""
        return hash(self.value)

    Account = "1"
    AdvId = "2"
    AdvRefID = "3"
    AdvSide = "4"
    AdvTransType = "5"
    AvgPx = "6"
    BeginSeqNo = "7"
    BeginString = "8"
    BodyLength = "9"
    CheckSum = "10"
    ClOrdID = "11"
    Commission = "12"
    CommType = "13"
    CumQty = "14"
    Currency = "15"
    EndSeqNo = "16"
    ExecID = "17"
    ExecInst = "18"
    ExecRefID = "19"
    ExecTransType = "20"
    HandlInst = "21"
    SecurityIDSource = "22"
    IOIID = "23"
    IOIOthSvc = "24"
    IOIQltyInd = "25"
    IOIRefID = "26"
    IOIQty = "27"
    IOITransType = "28"
    LastCapacity = "29"
    LastMkt = "30"
    LastPx = "31"
    LastQty = "32"
    NoLinesOfText = "33"
    MsgSeqNum = "34"
    MsgType = "35"
    NewSeqNo = "36"
    OrderID = "37"
    OrderQty = "38"
    OrdStatus = "39"
    OrdType = "40"
    OrigClOrdID = "41"
    OrigTime = "42"
    PossDupFlag = "43"
    Price = "44"
    RefSeqNum = "45"
    RelatdSym = "46"
    Rule80A = "47"
    SecurityID = "48"
    SenderCompID = "49"
    SenderSubID = "50"
    SendingDate = "51"
    SendingTime = "52"
    Quantity = "53"
    Side = "54"
    Symbol = "55"
    TargetCompID = "56"
    TargetSubID = "57"
    Text = "58"
    TimeInForce = "59"
    TransactTime = "60"
    Urgency = "61"
    ValidUntilTime = "62"
    SettlType = "63"
    SettlDate = "64"
    SymbolSfx = "65"
    ListID = "66"
    ListSeqNo = "67"
    TotNoOrders = "68"
    ListExecInst = "69"
    AllocID = "70"
    AllocTransType = "71"
    RefAllocID = "72"
    NoOrders = "73"
    AvgPxPrecision = "74"
    TradeDate = "75"
    ExecBroker = "76"
    PositionEffect = "77"
    NoAllocs = "78"
    AllocAccount = "79"
    AllocQty = "80"
    ProcessCode = "81"
    NoRpts = "82"
    RptSeq = "83"
    CxlQty = "84"
    NoDlvyInst = "85"
    DlvyInst = "86"
    AllocStatus = "87"
    AllocRejCode = "88"
    Signature = "89"
    SecureDataLen = "90"
    SecureData = "91"
    BrokerOfCredit = "92"
    SignatureLength = "93"
    EmailType = "94"
    RawDataLength = "95"
    RawData = "96"
    PossResend = "97"
    EncryptMethod = "98"
    StopPx = "99"
    ExDestination = "100"
    CxlRejReason = "102"
    OrdRejReason = "103"
    IOIQualifier = "104"
    WaveNo = "105"
    Issuer = "106"
    SecurityDesc = "107"
    HeartBtInt = "108"
    ClientID = "109"
    MinQty = "110"
    MaxFloor = "111"
    TestReqID = "112"
    ReportToExch = "113"
    LocateReqd = "114"
    OnBehalfOfCompID = "115"
    OnBehalfOfSubID = "116"
    QuoteID = "117"
    NetMoney = "118"
    SettlCurrAmt = "119"
    SettlCurrency = "120"
    ForexReq = "121"
    OrigSendingTime = "122"
    GapFillFlag = "123"
    NoExecs = "124"
    CxlType = "125"
    ExpireTime = "126"
    DKReason = "127"
    DeliverToCompID = "128"
    DeliverToSubID = "129"
    IOINaturalFlag = "130"
    QuoteReqID = "131"
    BidPx = "132"
    OfferPx = "133"
    BidSize = "134"
    OfferSize = "135"
    NoMiscFees = "136"
    MiscFeeAmt = "137"
    MiscFeeCurr = "138"
    MiscFeeType = "139"
    PrevClosePx = "140"
    ResetSeqNumFlag = "141"
    SenderLocationID = "142"
    TargetLocationID = "143"
    OnBehalfOfLocationID = "144"
    DeliverToLocationID = "145"
    NoRelatedSym = "146"
    Subject = "147"
    Headline = "148"
    URLLink = "149"
    ExecType = "150"
    LeavesQty = "151"
    CashOrderQty = "152"
    AllocAvgPx = "153"
    AllocNetMoney = "154"
    SettlCurrFxRate = "155"
    SettlCurrFxRateCalc = "156"
    NumDaysInterest = "157"
    AccruedInterestRate = "158"
    AccruedInterestAmt = "159"
    SettlInstMode = "160"
    AllocText = "161"
    SettlInstID = "162"
    SettlInstTransType = "163"
    EmailThreadID = "164"
    SettlInstSource = "165"
    SettlLocation = "166"
    SecurityType = "167"
    EffectiveTime = "168"
    StandInstDbType = "169"
    StandInstDbName = "170"
    StandInstDbID = "171"
    SettlDeliveryType = "172"
    SettlDepositoryCode = "173"
    SettlBrkrCode = "174"
    SettlInstCode = "175"
    SecuritySettlAgentName = "176"
    SecuritySettlAgentCode = "177"
    SecuritySettlAgentAcctNum = "178"
    SecuritySettlAgentAcctName = "179"
    SecuritySettlAgentContactName = "180"
    SecuritySettlAgentContactPhone = "181"
    CashSettlAgentName = "182"
    CashSettlAgentCode = "183"
    CashSettlAgentAcctNum = "184"
    CashSettlAgentAcctName = "185"
    CashSettlAgentContactName = "186"
    CashSettlAgentContactPhone = "187"
    BidSpotRate = "188"
    BidForwardPoints = "189"
    OfferSpotRate = "190"
    OfferForwardPoints = "191"
    OrderQty2 = "192"
    SettlDate2 = "193"
    LastSpotRate = "194"
    LastForwardPoints = "195"
    AllocLinkID = "196"
    AllocLinkType = "197"
    SecondaryOrderID = "198"
    NoIOIQualifiers = "199"
    MaturityMonthYear = "200"
    PutOrCall = "201"
    StrikePrice = "202"
    CoveredOrUncovered = "203"
    CustomerOrFirm = "204"
    MaturityDay = "205"
    OptAttribute = "206"
    SecurityExchange = "207"
    NotifyBrokerOfCredit = "208"
    AllocHandlInst = "209"
    MaxShow = "210"
    PegOffsetValue = "211"
    XmlDataLen = "212"
    XmlData = "213"
    SettlInstRefID = "214"
    NoRoutingIDs = "215"
    RoutingType = "216"
    RoutingID = "217"
    Spread = "218"
    Benchmark = "219"
    BenchmarkCurveCurrency = "220"
    BenchmarkCurveName = "221"
    BenchmarkCurvePoint = "222"
    CouponRate = "223"
    CouponPaymentDate = "224"
    IssueDate = "225"
    RepurchaseTerm = "226"
    RepurchaseRate = "227"
    Factor = "228"
    TradeOriginationDate = "229"
    ExDate = "230"
    ContractMultiplier = "231"
    NoStipulations = "232"
    StipulationType = "233"
    StipulationValue = "234"
    YieldType = "235"
    Yield = "236"
    TotalTakedown = "237"
    Concession = "238"
    RepoCollateralSecurityType = "239"
    RedemptionDate = "240"
    UnderlyingCouponPaymentDate = "241"
    UnderlyingIssueDate = "242"
    UnderlyingRepoCollateralSecurityType = "243"
    UnderlyingRepurchaseTerm = "244"
    UnderlyingRepurchaseRate = "245"
    UnderlyingFactor = "246"
    UnderlyingRedemptionDate = "247"
    LegCouponPaymentDate = "248"
    LegIssueDate = "249"
    LegRepoCollateralSecurityType = "250"
    LegRepurchaseTerm = "251"
    LegRepurchaseRate = "252"
    LegFactor = "253"
    LegRedemptionDate = "254"
    CreditRating = "255"
    UnderlyingCreditRating = "256"
    LegCreditRating = "257"
    TradedFlatSwitch = "258"
    BasisFeatureDate = "259"
    BasisFeaturePrice = "260"
    MDReqID = "262"
    SubscriptionRequestType = "263"
    MarketDepth = "264"
    MDUpdateType = "265"
    AggregatedBook = "266"
    NoMDEntryTypes = "267"
    NoMDEntries = "268"
    MDEntryType = "269"
    MDEntryPx = "270"
    MDEntrySize = "271"
    MDEntryDate = "272"
    MDEntryTime = "273"
    TickDirection = "274"
    MDMkt = "275"
    QuoteCondition = "276"
    TradeCondition = "277"
    MDEntryID = "278"
    MDUpdateAction = "279"
    MDEntryRefID = "280"
    MDReqRejReason = "281"
    MDEntryOriginator = "282"
    LocationID = "283"
    DeskID = "284"
    DeleteReason = "285"
    OpenCloseSettlFlag = "286"
    SellerDays = "287"
    MDEntryBuyer = "288"
    MDEntrySeller = "289"
    MDEntryPositionNo = "290"
    FinancialStatus = "291"
    CorporateAction = "292"
    DefBidSize = "293"
    DefOfferSize = "294"
    NoQuoteEntries = "295"
    NoQuoteSets = "296"
    QuoteStatus = "297"
    QuoteCancelType = "298"
    QuoteEntryID = "299"
    QuoteRejectReason = "300"
    QuoteResponseLevel = "301"
    QuoteSetID = "302"
    QuoteRequestType = "303"
    TotNoQuoteEntries = "304"
    UnderlyingSecurityIDSource = "305"
    UnderlyingIssuer = "306"
    UnderlyingSecurityDesc = "307"
    UnderlyingSecurityExchange = "308"
    UnderlyingSecurityID = "309"
    UnderlyingSecurityType = "310"
    UnderlyingSymbol = "311"
    UnderlyingSymbolSfx = "312"
    UnderlyingMaturityMonthYear = "313"
    UnderlyingMaturityDay = "314"
    UnderlyingPutOrCall = "315"
    UnderlyingStrikePrice = "316"
    UnderlyingOptAttribute = "317"
    UnderlyingCurrency = "318"
    RatioQty = "319"
    SecurityReqID = "320"
    SecurityRequestType = "321"
    SecurityResponseID = "322"
    SecurityResponseType = "323"
    SecurityStatusReqID = "324"
    UnsolicitedIndicator = "325"
    SecurityTradingStatus = "326"
    HaltReason = "327"
    InViewOfCommon = "328"
    DueToRelated = "329"
    BuyVolume = "330"
    SellVolume = "331"
    HighPx = "332"
    LowPx = "333"
    Adjustment = "334"
    TradSesReqID = "335"
    TradingSessionID = "336"
    ContraTrader = "337"
    TradSesMethod = "338"
    TradSesMode = "339"
    TradSesStatus = "340"
    TradSesStartTime = "341"
    TradSesOpenTime = "342"
    TradSesPreCloseTime = "343"
    TradSesCloseTime = "344"
    TradSesEndTime = "345"
    NumberOfOrders = "346"
    MessageEncoding = "347"
    EncodedIssuerLen = "348"
    EncodedIssuer = "349"
    EncodedSecurityDescLen = "350"
    EncodedSecurityDesc = "351"
    EncodedListExecInstLen = "352"
    EncodedListExecInst = "353"
    EncodedTextLen = "354"
    EncodedText = "355"
    EncodedSubjectLen = "356"
    EncodedSubject = "357"
    EncodedHeadlineLen = "358"
    EncodedHeadline = "359"
    EncodedAllocTextLen = "360"
    EncodedAllocText = "361"
    EncodedUnderlyingIssuerLen = "362"
    EncodedUnderlyingIssuer = "363"
    EncodedUnderlyingSecurityDescLen = "364"
    EncodedUnderlyingSecurityDesc = "365"
    AllocPrice = "366"
    QuoteSetValidUntilTime = "367"
    QuoteEntryRejectReason = "368"
    LastMsgSeqNumProcessed = "369"
    OnBehalfOfSendingTime = "370"
    RefTagID = "371"
    RefMsgType = "372"
    SessionRejectReason = "373"
    BidRequestTransType = "374"
    ContraBroker = "375"
    ComplianceID = "376"
    SolicitedFlag = "377"
    ExecRestatementReason = "378"
    BusinessRejectRefID = "379"
    BusinessRejectReason = "380"
    GrossTradeAmt = "381"
    NoContraBrokers = "382"
    MaxMessageSize = "383"
    NoMsgTypes = "384"
    MsgDirection = "385"
    NoTradingSessions = "386"
    TotalVolumeTraded = "387"
    DiscretionInst = "388"
    DiscretionOffsetValue = "389"
    BidID = "390"
    ClientBidID = "391"
    ListName = "392"
    TotNoRelatedSym = "393"
    BidType = "394"
    NumTickets = "395"
    SideValue1 = "396"
    SideValue2 = "397"
    NoBidDescriptors = "398"
    BidDescriptorType = "399"
    BidDescriptor = "400"
    SideValueInd = "401"
    LiquidityPctLow = "402"
    LiquidityPctHigh = "403"
    LiquidityValue = "404"
    EFPTrackingError = "405"
    FairValue = "406"
    OutsideIndexPct = "407"
    ValueOfFutures = "408"
    LiquidityIndType = "409"
    WtAverageLiquidity = "410"
    ExchangeForPhysical = "411"
    OutMainCntryUIndex = "412"
    CrossPercent = "413"
    ProgRptReqs = "414"
    ProgPeriodInterval = "415"
    IncTaxInd = "416"
    NumBidders = "417"
    BidTradeType = "418"
    BasisPxType = "419"
    NoBidComponents = "420"
    Country = "421"
    TotNoStrikes = "422"
    PriceType = "423"
    DayOrderQty = "424"
    DayCumQty = "425"
    DayAvgPx = "426"
    GTBookingInst = "427"
    NoStrikes = "428"
    ListStatusType = "429"
    NetGrossInd = "430"
    ListOrderStatus = "431"
    ExpireDate = "432"
    ListExecInstType = "433"
    CxlRejResponseTo = "434"
    UnderlyingCouponRate = "435"
    UnderlyingContractMultiplier = "436"
    ContraTradeQty = "437"
    ContraTradeTime = "438"
    ClearingFirm = "439"
    ClearingAccount = "440"
    LiquidityNumSecurities = "441"
    MultiLegReportingType = "442"
    StrikeTime = "443"
    ListStatusText = "444"
    EncodedListStatusTextLen = "445"
    EncodedListStatusText = "446"
    PartyIDSource = "447"
    PartyID = "448"
    TotalVolumeTradedDate = "449"
    NetChgPrevDay = "451"
    PartyRole = "452"
    NoPartyIDs = "453"
    NoSecurityAltID = "454"
    SecurityAltID = "455"
    SecurityAltIDSource = "456"
    NoUnderlyingSecurityAltID = "457"
    UnderlyingSecurityAltID = "458"
    UnderlyingSecurityAltIDSource = "459"
    Product = "460"
    CFICode = "461"
    UnderlyingProduct = "462"
    UnderlyingCFICode = "463"
    TestMessageIndicator = "464"
    QuantityType = "465"
    BookingRefID = "466"
    IndividualAllocID = "467"
    RoundingDirection = "468"
    RoundingModulus = "469"
    CountryOfIssue = "470"
    StateOrProvinceOfIssue = "471"
    LocaleOfIssue = "472"
    NoRegistDtls = "473"
    MailingDtls = "474"
    InvestorCountryOfResidence = "475"
    PaymentRef = "476"
    DistribPaymentMethod = "477"
    CashDistribCurr = "478"
    CommCurrency = "479"
    CancellationRights = "480"
    MoneyLaunderingStatus = "481"
    MailingInst = "482"
    TransBkdTime = "483"
    ExecPriceType = "484"
    ExecPriceAdjustment = "485"
    DateOfBirth = "486"
    TradeReportTransType = "487"
    CardHolderName = "488"
    CardNumber = "489"
    CardExpDate = "490"
    CardIssNum = "491"
    PaymentMethod = "492"
    RegistAcctType = "493"
    Designation = "494"
    TaxAdvantageType = "495"
    RegistRejReasonText = "496"
    FundRenewWaiv = "497"
    CashDistribAgentName = "498"
    CashDistribAgentCode = "499"
    CashDistribAgentAcctNumber = "500"
    CashDistribPayRef = "501"
    CashDistribAgentAcctName = "502"
    CardStartDate = "503"
    PaymentDate = "504"
    PaymentRemitterID = "505"
    RegistStatus = "506"
    RegistRejReasonCode = "507"
    RegistRefID = "508"
    RegistDtls = "509"
    NoDistribInsts = "510"
    RegistEmail = "511"
    DistribPercentage = "512"
    RegistID = "513"
    RegistTransType = "514"
    ExecValuationPoint = "515"
    OrderPercent = "516"
    OwnershipType = "517"
    NoContAmts = "518"
    ContAmtType = "519"
    ContAmtValue = "520"
    ContAmtCurr = "521"
    OwnerType = "522"
    PartySubID = "523"
    NestedPartyID = "524"
    NestedPartyIDSource = "525"
    SecondaryClOrdID = "526"
    SecondaryExecID = "527"
    OrderCapacity = "528"
    OrderRestrictions = "529"
    MassCancelRequestType = "530"
    MassCancelResponse = "531"
    MassCancelRejectReason = "532"
    TotalAffectedOrders = "533"
    NoAffectedOrders = "534"
    AffectedOrderID = "535"
    AffectedSecondaryOrderID = "536"
    QuoteType = "537"
    NestedPartyRole = "538"
    NoNestedPartyIDs = "539"
    TotalAccruedInterestAmt = "540"
    MaturityDate = "541"
    UnderlyingMaturityDate = "542"
    InstrRegistry = "543"
    CashMargin = "544"
    NestedPartySubID = "545"
    Scope = "546"
    MDImplicitDelete = "547"
    CrossID = "548"
    CrossType = "549"
    CrossPrioritization = "550"
    OrigCrossID = "551"
    NoSides = "552"
    Username = "553"
    Password = "554"
    NoLegs = "555"
    LegCurrency = "556"
    TotNoSecurityTypes = "557"
    NoSecurityTypes = "558"
    SecurityListRequestType = "559"
    SecurityRequestResult = "560"
    RoundLot = "561"
    MinTradeVol = "562"
    MultiLegRptTypeReq = "563"
    LegPositionEffect = "564"
    LegCoveredOrUncovered = "565"
    LegPrice = "566"
    TradSesStatusRejReason = "567"
    TradeRequestID = "568"
    TradeRequestType = "569"
    PreviouslyReported = "570"
    TradeReportID = "571"
    TradeReportRefID = "572"
    MatchStatus = "573"
    MatchType = "574"
    OddLot = "575"
    NoClearingInstructions = "576"
    ClearingInstruction = "577"
    TradeInputSource = "578"
    TradeInputDevice = "579"
    NoDates = "580"
    AccountType = "581"
    CustOrderCapacity = "582"
    ClOrdLinkID = "583"
    MassStatusReqID = "584"
    MassStatusReqType = "585"
    OrigOrdModTime = "586"
    LegSettlType = "587"
    LegSettlDate = "588"
    DayBookingInst = "589"
    BookingUnit = "590"
    PreallocMethod = "591"
    UnderlyingCountryOfIssue = "592"
    UnderlyingStateOrProvinceOfIssue = "593"
    UnderlyingLocaleOfIssue = "594"
    UnderlyingInstrRegistry = "595"
    LegCountryOfIssue = "596"
    LegStateOrProvinceOfIssue = "597"
    LegLocaleOfIssue = "598"
    LegInstrRegistry = "599"
    LegSymbol = "600"
    LegSymbolSfx = "601"
    LegSecurityID = "602"
    LegSecurityIDSource = "603"
    NoLegSecurityAltID = "604"
    LegSecurityAltID = "605"
    LegSecurityAltIDSource = "606"
    LegProduct = "607"
    LegCFICode = "608"
    LegSecurityType = "609"
    LegMaturityMonthYear = "610"
    LegMaturityDate = "611"
    LegStrikePrice = "612"
    LegOptAttribute = "613"
    LegContractMultiplier = "614"
    LegCouponRate = "615"
    LegSecurityExchange = "616"
    LegIssuer = "617"
    EncodedLegIssuerLen = "618"
    EncodedLegIssuer = "619"
    LegSecurityDesc = "620"
    EncodedLegSecurityDescLen = "621"
    EncodedLegSecurityDesc = "622"
    LegRatioQty = "623"
    LegSide = "624"
    TradingSessionSubID = "625"
    AllocType = "626"
    NoHops = "627"
    HopCompID = "628"
    HopSendingTime = "629"
    HopRefID = "630"
    MidPx = "631"
    BidYield = "632"
    MidYield = "633"
    OfferYield = "634"
    ClearingFeeIndicator = "635"
    WorkingIndicator = "636"
    LegLastPx = "637"
    PriorityIndicator = "638"
    PriceImprovement = "639"
    Price2 = "640"
    LastForwardPoints2 = "641"
    BidForwardPoints2 = "642"
    OfferForwardPoints2 = "643"
    RFQReqID = "644"
    MktBidPx = "645"
    MktOfferPx = "646"
    MinBidSize = "647"
    MinOfferSize = "648"
    QuoteStatusReqID = "649"
    LegalConfirm = "650"
    UnderlyingLastPx = "651"
    UnderlyingLastQty = "652"
    SecDefStatus = "653"
    LegRefID = "654"
    ContraLegRefID = "655"
    SettlCurrBidFxRate = "656"
    SettlCurrOfferFxRate = "657"
    QuoteRequestRejectReason = "658"
    SideComplianceID = "659"
    AcctIDSource = "660"
    AllocAcctIDSource = "661"
    BenchmarkPrice = "662"
    BenchmarkPriceType = "663"
    ConfirmID = "664"
    ConfirmStatus = "665"
    ConfirmTransType = "666"
    ContractSettlMonth = "667"
    DeliveryForm = "668"
    LastParPx = "669"
    NoLegAllocs = "670"
    LegAllocAccount = "671"
    LegIndividualAllocID = "672"
    LegAllocQty = "673"
    LegAllocAcctIDSource = "674"
    LegSettlCurrency = "675"
    LegBenchmarkCurveCurrency = "676"
    LegBenchmarkCurveName = "677"
    LegBenchmarkCurvePoint = "678"
    LegBenchmarkPrice = "679"
    LegBenchmarkPriceType = "680"
    LegBidPx = "681"
    LegIOIQty = "682"
    NoLegStipulations = "683"
    LegOfferPx = "684"
    LegOrderQty = "685"
    LegPriceType = "686"
    LegQty = "687"
    LegStipulationType = "688"
    LegStipulationValue = "689"
    LegSwapType = "690"
    Pool = "691"
    QuotePriceType = "692"
    QuoteRespID = "693"
    QuoteRespType = "694"
    QuoteQualifier = "695"
    YieldRedemptionDate = "696"
    YieldRedemptionPrice = "697"
    YieldRedemptionPriceType = "698"
    BenchmarkSecurityID = "699"
    ReversalIndicator = "700"
    YieldCalcDate = "701"
    NoPositions = "702"
    PosType = "703"
    LongQty = "704"
    ShortQty = "705"
    PosQtyStatus = "706"
    PosAmtType = "707"
    PosAmt = "708"
    PosTransType = "709"
    PosReqID = "710"
    NoUnderlyings = "711"
    PosMaintAction = "712"
    OrigPosReqRefID = "713"
    PosMaintRptRefID = "714"
    ClearingBusinessDate = "715"
    SettlSessID = "716"
    SettlSessSubID = "717"
    AdjustmentType = "718"
    ContraryInstructionIndicator = "719"
    PriorSpreadIndicator = "720"
    PosMaintRptID = "721"
    PosMaintStatus = "722"
    PosMaintResult = "723"
    PosReqType = "724"
    ResponseTransportType = "725"
    ResponseDestination = "726"
    TotalNumPosReports = "727"
    PosReqResult = "728"
    PosReqStatus = "729"
    SettlPrice = "730"
    SettlPriceType = "731"
    UnderlyingSettlPrice = "732"
    UnderlyingSettlPriceType = "733"
    PriorSettlPrice = "734"
    NoQuoteQualifiers = "735"
    AllocSettlCurrency = "736"
    AllocSettlCurrAmt = "737"
    InterestAtMaturity = "738"
    LegDatedDate = "739"
    LegPool = "740"
    AllocInterestAtMaturity = "741"
    AllocAccruedInterestAmt = "742"
    DeliveryDate = "743"
    AssignmentMethod = "744"
    AssignmentUnit = "745"
    OpenInterest = "746"
    ExerciseMethod = "747"
    TotNumTradeReports = "748"
    TradeRequestResult = "749"
    TradeRequestStatus = "750"
    TradeReportRejectReason = "751"
    SideMultiLegReportingType = "752"
    NoPosAmt = "753"
    AutoAcceptIndicator = "754"
    AllocReportID = "755"
    NoNested2PartyIDs = "756"
    Nested2PartyID = "757"
    Nested2PartyIDSource = "758"
    Nested2PartyRole = "759"
    Nested2PartySubID = "760"
    BenchmarkSecurityIDSource = "761"
    SecuritySubType = "762"
    UnderlyingSecuritySubType = "763"
    LegSecuritySubType = "764"
    AllowableOneSidednessPct = "765"
    AllowableOneSidednessValue = "766"
    AllowableOneSidednessCurr = "767"
    NoTrdRegTimestamps = "768"
    TrdRegTimestamp = "769"
    TrdRegTimestampType = "770"
    TrdRegTimestampOrigin = "771"
    ConfirmRefID = "772"
    ConfirmType = "773"
    ConfirmRejReason = "774"
    BookingType = "775"
    IndividualAllocRejCode = "776"
    SettlInstMsgID = "777"
    NoSettlInst = "778"
    LastUpdateTime = "779"
    AllocSettlInstType = "780"
    NoSettlPartyIDs = "781"
    SettlPartyID = "782"
    SettlPartyIDSource = "783"
    SettlPartyRole = "784"
    SettlPartySubID = "785"
    SettlPartySubIDType = "786"
    DlvyInstType = "787"
    TerminationType = "788"
    NextExpectedMsgSeqNum = "789"
    OrdStatusReqID = "790"
    SettlInstReqID = "791"
    SettlInstReqRejCode = "792"
    SecondaryAllocID = "793"
    AllocReportType = "794"
    AllocReportRefID = "795"
    AllocCancReplaceReason = "796"
    CopyMsgIndicator = "797"
    AllocAccountType = "798"
    OrderAvgPx = "799"
    OrderBookingQty = "800"
    NoSettlPartySubIDs = "801"
    NoPartySubIDs = "802"
    PartySubIDType = "803"
    NoNestedPartySubIDs = "804"
    NestedPartySubIDType = "805"
    NoNested2PartySubIDs = "806"
    Nested2PartySubIDType = "807"
    AllocIntermedReqType = "808"
    UnderlyingPx = "810"
    PriceDelta = "811"
    ApplQueueMax = "812"
    ApplQueueDepth = "813"
    ApplQueueResolution = "814"
    ApplQueueAction = "815"
    NoAltMDSource = "816"
    AltMDSourceID = "817"
    SecondaryTradeReportID = "818"
    AvgPxIndicator = "819"
    TradeLinkID = "820"
    OrderInputDevice = "821"
    UnderlyingTradingSessionID = "822"
    UnderlyingTradingSessionSubID = "823"
    TradeLegRefID = "824"
    ExchangeRule = "825"
    TradeAllocIndicator = "826"
    ExpirationCycle = "827"
    TrdType = "828"
    TrdSubType = "829"
    TransferReason = "830"
    AsgnReqID = "831"
    TotNumAssignmentReports = "832"
    AsgnRptID = "833"
    ThresholdAmount = "834"
    PegMoveType = "835"
    PegOffsetType = "836"
    PegLimitType = "837"
    PegRoundDirection = "838"
    PeggedPrice = "839"
    PegScope = "840"
    DiscretionMoveType = "841"
    DiscretionOffsetType = "842"
    DiscretionLimitType = "843"
    DiscretionRoundDirection = "844"
    DiscretionPrice = "845"
    DiscretionScope = "846"
    TargetStrategy = "847"
    TargetStrategyParameters = "848"
    ParticipationRate = "849"
    TargetStrategyPerformance = "850"
    LastLiquidityInd = "851"
    PublishTrdIndicator = "852"
    ShortSaleReason = "853"
    QtyType = "854"
    SecondaryTrdType = "855"
    TradeReportType = "856"
    AllocNoOrdersType = "857"
    SharedCommission = "858"
    ConfirmReqID = "859"
    AvgParPx = "860"
    ReportedPx = "861"
    NoCapacities = "862"
    OrderCapacityQty = "863"
    NoEvents = "864"
    EventType = "865"
    EventDate = "866"
    EventPx = "867"
    EventText = "868"
    PctAtRisk = "869"
    NoInstrAttrib = "870"
    InstrAttribType = "871"
    InstrAttribValue = "872"
    DatedDate = "873"
    InterestAccrualDate = "874"
    CPProgram = "875"
    CPRegType = "876"
    UnderlyingCPProgram = "877"
    UnderlyingCPRegType = "878"
    UnderlyingQty = "879"
    TrdMatchID = "880"
    SecondaryTradeReportRefID = "881"
    UnderlyingDirtyPrice = "882"
    UnderlyingEndPrice = "883"
    UnderlyingStartValue = "884"
    UnderlyingCurrentValue = "885"
    UnderlyingEndValue = "886"
    NoUnderlyingStips = "887"
    UnderlyingStipType = "888"
    UnderlyingStipValue = "889"
    MaturityNetMoney = "890"
    MiscFeeBasis = "891"
    TotNoAllocs = "892"
    LastFragment = "893"
    CollReqID = "894"
    CollAsgnReason = "895"
    CollInquiryQualifier = "896"
    NoTrades = "897"
    MarginRatio = "898"
    MarginExcess = "899"
    TotalNetValue = "900"
    CashOutstanding = "901"
    CollAsgnID = "902"
    CollAsgnTransType = "903"
    CollRespID = "904"
    CollAsgnRespType = "905"
    CollAsgnRejectReason = "906"
    CollAsgnRefID = "907"
    CollRptID = "908"
    CollInquiryID = "909"
    CollStatus = "910"
    TotNumReports = "911"
    LastRptRequested = "912"
    AgreementDesc = "913"
    AgreementID = "914"
    AgreementDate = "915"
    StartDate = "916"
    EndDate = "917"
    AgreementCurrency = "918"
    DeliveryType = "919"
    EndAccruedInterestAmt = "920"
    StartCash = "921"
    EndCash = "922"
    UserRequestID = "923"
    UserRequestType = "924"
    NewPassword = "925"
    UserStatus = "926"
    UserStatusText = "927"
    StatusValue = "928"
    StatusText = "929"
    RefCompID = "930"
    RefSubID = "931"
    NetworkResponseID = "932"
    NetworkRequestID = "933"
    LastNetworkResponseID = "934"
    NetworkRequestType = "935"
    NoCompIDs = "936"
    NetworkStatusResponseType = "937"
    NoCollInquiryQualifier = "938"
    TrdRptStatus = "939"
    AffirmStatus = "940"
    UnderlyingStrikeCurrency = "941"
    LegStrikeCurrency = "942"
    TimeBracket = "943"
    CollAction = "944"
    CollInquiryStatus = "945"
    CollInquiryResult = "946"
    StrikeCurrency = "947"
    NoNested3PartyIDs = "948"
    Nested3PartyID = "949"
    Nested3PartyIDSource = "950"
    Nested3PartyRole = "951"
    NoNested3PartySubIDs = "952"
    Nested3PartySubID = "953"
    Nested3PartySubIDType = "954"
    LegContractSettlMonth = "955"
    LegInterestAccrualDate = "956"
    MinPriceIncrement = "969"
    UnitOfMeasure = "996"
    UnitOfMeasureCurrency = "1716"
