"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from builtins import (
    bool,
    float,
    int,
)

from google.protobuf.descriptor import (
    Descriptor,
    FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp,
)

from typing import (
    Iterable,
    Optional,
    Text,
)

from typing_extensions import (
    Literal,
)


DESCRIPTOR: FileDescriptor = ...

class GetSymbolInfosReq(Message):
    """********************************************************************************
    get_symbol_infos - 查询标的基本信息
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#joYCF2
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    SEC_TYPE1_FIELD_NUMBER: int
    SEC_TYPE2_FIELD_NUMBER: int
    EXCHANGES_FIELD_NUMBER: int
    SYMBOLS_FIELD_NUMBER: int
    sec_type1: int = ...
    """证券品种大类 必填"""

    sec_type2: int = ...
    """证券品种细类"""

    @property
    def exchanges(self) -> RepeatedScalarFieldContainer[Text]:
        """交易所代码"""
        pass
    @property
    def symbols(self) -> RepeatedScalarFieldContainer[Text]:
        """标的代码"""
        pass
    def __init__(self,
        *,
        sec_type1 : int = ...,
        sec_type2 : int = ...,
        exchanges : Optional[Iterable[Text]] = ...,
        symbols : Optional[Iterable[Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"exchanges",b"exchanges",u"sec_type1",b"sec_type1",u"sec_type2",b"sec_type2",u"symbols",b"symbols"]) -> None: ...

class SymbolInfo(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    SEC_TYPE1_FIELD_NUMBER: int
    SEC_TYPE2_FIELD_NUMBER: int
    BOARD_FIELD_NUMBER: int
    EXCHANGE_FIELD_NUMBER: int
    SEC_ID_FIELD_NUMBER: int
    SEC_NAME_FIELD_NUMBER: int
    SEC_ABBR_FIELD_NUMBER: int
    PRICE_TICK_FIELD_NUMBER: int
    TRADE_N_FIELD_NUMBER: int
    LISTED_DATE_FIELD_NUMBER: int
    DELISTED_DATE_FIELD_NUMBER: int
    UNDERLYING_SYMBOL_FIELD_NUMBER: int
    OPTION_TYPE_FIELD_NUMBER: int
    OPTION_MARGIN_RATIO1_FIELD_NUMBER: int
    OPTION_MARGIN_RATIO2_FIELD_NUMBER: int
    CALL_OR_PUT_FIELD_NUMBER: int
    CONVERSION_START_DATE_FIELD_NUMBER: int
    symbol: Text = ...
    """标的代码"""

    sec_type1: int = ...
    """证券品种大类"""

    sec_type2: int = ...
    """证券品种细类"""

    board: int = ...
    """板块"""

    exchange: Text = ...
    """交易所代码"""

    sec_id: Text = ...
    """交易所标的代码"""

    sec_name: Text = ...
    """交易所标的名称"""

    sec_abbr: Text = ...
    """交易所标的简称"""

    price_tick: float = ...
    """最小变动单位"""

    trade_n: int = ...
    """交易制度 0表示T+0 1表示T+1 2表示T+2"""

    @property
    def listed_date(self) -> Timestamp:
        """上市日期 证券/指数的上市日 衍生品合约的挂牌日"""
        pass
    @property
    def delisted_date(self) -> Timestamp:
        """退市日期 股票/基金的退市日 期货/期权的到期日(最后交易日) 可转债的赎回登记日"""
        pass
    underlying_symbol: Text = ...
    """标的资产"""

    option_type: Text = ...
    """行权方式"""

    option_margin_ratio1: float = ...
    """期权保证金计算参数1"""

    option_margin_ratio2: float = ...
    """期权保证金计算参数2"""

    call_or_put: Text = ...
    """合约类型"""

    @property
    def conversion_start_date(self) -> Timestamp:
        """可转债开始转股日期"""
        pass
    def __init__(self,
        *,
        symbol : Text = ...,
        sec_type1 : int = ...,
        sec_type2 : int = ...,
        board : int = ...,
        exchange : Text = ...,
        sec_id : Text = ...,
        sec_name : Text = ...,
        sec_abbr : Text = ...,
        price_tick : float = ...,
        trade_n : int = ...,
        listed_date : Optional[Timestamp] = ...,
        delisted_date : Optional[Timestamp] = ...,
        underlying_symbol : Text = ...,
        option_type : Text = ...,
        option_margin_ratio1 : float = ...,
        option_margin_ratio2 : float = ...,
        call_or_put : Text = ...,
        conversion_start_date : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"conversion_start_date",b"conversion_start_date",u"delisted_date",b"delisted_date",u"listed_date",b"listed_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"board",b"board",u"call_or_put",b"call_or_put",u"conversion_start_date",b"conversion_start_date",u"delisted_date",b"delisted_date",u"exchange",b"exchange",u"listed_date",b"listed_date",u"option_margin_ratio1",b"option_margin_ratio1",u"option_margin_ratio2",b"option_margin_ratio2",u"option_type",b"option_type",u"price_tick",b"price_tick",u"sec_abbr",b"sec_abbr",u"sec_id",b"sec_id",u"sec_name",b"sec_name",u"sec_type1",b"sec_type1",u"sec_type2",b"sec_type2",u"symbol",b"symbol",u"trade_n",b"trade_n",u"underlying_symbol",b"underlying_symbol"]) -> None: ...

class GetSymbolInfosResp(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_INFOS_FIELD_NUMBER: int
    @property
    def symbol_infos(self) -> RepeatedCompositeFieldContainer[SymbolInfo]: ...
    def __init__(self,
        *,
        symbol_infos : Optional[Iterable[SymbolInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"symbol_infos",b"symbol_infos"]) -> None: ...

class GetSymbolsReq(Message):
    """********************************************************************************
    get_symbols - 查询指定交易日标的交易信息
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#DwilE4
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    SEC_TYPE1_FIELD_NUMBER: int
    SEC_TYPE2_FIELD_NUMBER: int
    EXCHANGES_FIELD_NUMBER: int
    SYMBOLS_FIELD_NUMBER: int
    SKIP_SUSPENDED_FIELD_NUMBER: int
    SKIP_ST_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    sec_type1: int = ...
    """证券品种大类 必填"""

    sec_type2: int = ...
    """证券品种细类"""

    @property
    def exchanges(self) -> RepeatedScalarFieldContainer[Text]:
        """交易所代码"""
        pass
    @property
    def symbols(self) -> RepeatedScalarFieldContainer[Text]:
        """标的代码"""
        pass
    skip_suspended: bool = ...
    """跳过停牌"""

    skip_st: bool = ...
    """跳过ST"""

    trade_date: Text = ...
    """交易日"""

    def __init__(self,
        *,
        sec_type1 : int = ...,
        sec_type2 : int = ...,
        exchanges : Optional[Iterable[Text]] = ...,
        symbols : Optional[Iterable[Text]] = ...,
        skip_suspended : bool = ...,
        skip_st : bool = ...,
        trade_date : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"exchanges",b"exchanges",u"sec_type1",b"sec_type1",u"sec_type2",b"sec_type2",u"skip_st",b"skip_st",u"skip_suspended",b"skip_suspended",u"symbols",b"symbols",u"trade_date",b"trade_date"]) -> None: ...

class Symbol(Message):
    DESCRIPTOR: Descriptor = ...
    TRADE_DATE_FIELD_NUMBER: int
    IS_ADJUSTED_FIELD_NUMBER: int
    IS_SUSPENDED_FIELD_NUMBER: int
    POSITION_FIELD_NUMBER: int
    SETTLE_PRICE_FIELD_NUMBER: int
    PRE_SETTLE_FIELD_NUMBER: int
    PRE_CLOSE_FIELD_NUMBER: int
    UPPER_LIMIT_FIELD_NUMBER: int
    LOWER_LIMIT_FIELD_NUMBER: int
    TURN_RATE_FIELD_NUMBER: int
    ADJ_FACTOR_FIELD_NUMBER: int
    MARGIN_RATIO_FIELD_NUMBER: int
    CONVERSION_PRICE_FIELD_NUMBER: int
    EXERCISE_PRICE_FIELD_NUMBER: int
    MULTIPLIER_FIELD_NUMBER: int
    INFO_FIELD_NUMBER: int
    IS_ST_FIELD_NUMBER: int
    @property
    def trade_date(self) -> Timestamp:
        """交易日期"""
        pass
    is_adjusted: bool = ...
    """合约调整"""

    is_suspended: bool = ...
    """是否停牌"""

    position: int = ...
    """持仓量"""

    settle_price: float = ...
    """结算价"""

    pre_settle: float = ...
    """昨结算价"""

    pre_close: float = ...
    """昨收盘价"""

    upper_limit: float = ...
    """涨停价"""

    lower_limit: float = ...
    """跌停价"""

    turn_rate: float = ...
    """换手率"""

    adj_factor: float = ...
    """复权因子"""

    margin_ratio: float = ...
    """保证金比例"""

    conversion_price: float = ...
    """转股价"""

    exercise_price: float = ...
    """行权价"""

    multiplier: int = ...
    """合约乘数"""

    @property
    def info(self) -> SymbolInfo:
        """包含 info 中的字段"""
        pass
    is_st: bool = ...
    """是否ST"""

    def __init__(self,
        *,
        trade_date : Optional[Timestamp] = ...,
        is_adjusted : bool = ...,
        is_suspended : bool = ...,
        position : int = ...,
        settle_price : float = ...,
        pre_settle : float = ...,
        pre_close : float = ...,
        upper_limit : float = ...,
        lower_limit : float = ...,
        turn_rate : float = ...,
        adj_factor : float = ...,
        margin_ratio : float = ...,
        conversion_price : float = ...,
        exercise_price : float = ...,
        multiplier : int = ...,
        info : Optional[SymbolInfo] = ...,
        is_st : bool = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"info",b"info",u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"adj_factor",b"adj_factor",u"conversion_price",b"conversion_price",u"exercise_price",b"exercise_price",u"info",b"info",u"is_adjusted",b"is_adjusted",u"is_st",b"is_st",u"is_suspended",b"is_suspended",u"lower_limit",b"lower_limit",u"margin_ratio",b"margin_ratio",u"multiplier",b"multiplier",u"position",b"position",u"pre_close",b"pre_close",u"pre_settle",b"pre_settle",u"settle_price",b"settle_price",u"trade_date",b"trade_date",u"turn_rate",b"turn_rate",u"upper_limit",b"upper_limit"]) -> None: ...

class GetSymbolsResp(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    @property
    def symbols(self) -> RepeatedCompositeFieldContainer[Symbol]: ...
    def __init__(self,
        *,
        symbols : Optional[Iterable[Symbol]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"symbols",b"symbols"]) -> None: ...

class GetHistorySymbolReq(Message):
    """********************************************************************************
    get_history_symbol - 查询指定标的历史交易日的交易信息
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#sJ7g7G
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    symbol: Text = ...
    """标的代码"""

    start_date: Text = ...
    """开始时间"""

    end_date: Text = ...
    """结束时间"""

    def __init__(self,
        *,
        symbol : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_date",b"end_date",u"start_date",b"start_date",u"symbol",b"symbol"]) -> None: ...

class GetHistorySymbolResp(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    @property
    def symbols(self) -> RepeatedCompositeFieldContainer[Symbol]: ...
    def __init__(self,
        *,
        symbols : Optional[Iterable[Symbol]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"symbols",b"symbols"]) -> None: ...

class GetTradingDatesByYearReq(Message):
    """********************************************************************************
    get_trading_dates_by_year - 查询年度交易日历
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#BqT4BD
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    EXCHANGE_FIELD_NUMBER: int
    START_YEAR_FIELD_NUMBER: int
    END_YEAR_FIELD_NUMBER: int
    exchange: Text = ...
    """交易所代码"""

    start_year: int = ...
    """开始年份"""

    end_year: int = ...
    """结束年份"""

    def __init__(self,
        *,
        exchange : Text = ...,
        start_year : int = ...,
        end_year : int = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_year",b"end_year",u"exchange",b"exchange",u"start_year",b"start_year"]) -> None: ...

class TradingDate(Message):
    DESCRIPTOR: Descriptor = ...
    DATE_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    NEXT_TRADE_DATE_FIELD_NUMBER: int
    PRE_TRADE_DATE_FIELD_NUMBER: int
    @property
    def date(self) -> Timestamp:
        """自然日"""
        pass
    @property
    def trade_date(self) -> Timestamp:
        """交易日"""
        pass
    @property
    def next_trade_date(self) -> Timestamp:
        """下一个交易日"""
        pass
    @property
    def pre_trade_date(self) -> Timestamp:
        """上一个交易日"""
        pass
    def __init__(self,
        *,
        date : Optional[Timestamp] = ...,
        trade_date : Optional[Timestamp] = ...,
        next_trade_date : Optional[Timestamp] = ...,
        pre_trade_date : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"date",b"date",u"next_trade_date",b"next_trade_date",u"pre_trade_date",b"pre_trade_date",u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"date",b"date",u"next_trade_date",b"next_trade_date",u"pre_trade_date",b"pre_trade_date",u"trade_date",b"trade_date"]) -> None: ...

class GetTradingDatesByYearResp(Message):
    DESCRIPTOR: Descriptor = ...
    DATES_FIELD_NUMBER: int
    @property
    def dates(self) -> RepeatedCompositeFieldContainer[TradingDate]: ...
    def __init__(self,
        *,
        dates : Optional[Iterable[TradingDate]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"dates",b"dates"]) -> None: ...

class GetTradingDatesPrevNReq(Message):
    """********************************************************************************
    get_previous_n_trading_dates - 查询指定日期的前n个交易日
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#BqT4BD
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    EXCHANGE_FIELD_NUMBER: int
    DATE_FIELD_NUMBER: int
    N_FIELD_NUMBER: int
    exchange: Text = ...
    """交易所代码"""

    date: Text = ...
    """时间"""

    n: int = ...
    """交易日个数"""

    def __init__(self,
        *,
        exchange : Text = ...,
        date : Text = ...,
        n : int = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date",b"date",u"exchange",b"exchange",u"n",b"n"]) -> None: ...

class GetTradingDatesPrevNResp(Message):
    DESCRIPTOR: Descriptor = ...
    TRADING_DATES_FIELD_NUMBER: int
    @property
    def trading_dates(self) -> RepeatedCompositeFieldContainer[Timestamp]: ...
    def __init__(self,
        *,
        trading_dates : Optional[Iterable[Timestamp]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"trading_dates",b"trading_dates"]) -> None: ...

class GetTradingDatesNextNReq(Message):
    """********************************************************************************
    get_next_n_trading_dates - 查询指定日期的后n个交易日
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#BqT4BD
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    EXCHANGE_FIELD_NUMBER: int
    DATE_FIELD_NUMBER: int
    N_FIELD_NUMBER: int
    exchange: Text = ...
    """交易所代码"""

    date: Text = ...
    """时间"""

    n: int = ...
    """N 个交易日"""

    def __init__(self,
        *,
        exchange : Text = ...,
        date : Text = ...,
        n : int = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date",b"date",u"exchange",b"exchange",u"n",b"n"]) -> None: ...

class GetTradingDatesNextNResp(Message):
    DESCRIPTOR: Descriptor = ...
    TRADING_DATES_FIELD_NUMBER: int
    @property
    def trading_dates(self) -> RepeatedCompositeFieldContainer[Timestamp]: ...
    def __init__(self,
        *,
        trading_dates : Optional[Iterable[Timestamp]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"trading_dates",b"trading_dates"]) -> None: ...

class GetTradingSessionReq(Message):
    """********************************************************************************
    get_trading_session - 查询交易时段
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#8woeDc
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    DATE_FIELD_NUMBER: int
    @property
    def symbols(self) -> RepeatedScalarFieldContainer[Text]:
        """标的代码"""
        pass
    date: Text = ...
    """查询日期"""

    def __init__(self,
        *,
        symbols : Optional[Iterable[Text]] = ...,
        date : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date",b"date",u"symbols",b"symbols"]) -> None: ...

class Session(Message):
    DESCRIPTOR: Descriptor = ...
    START_FIELD_NUMBER: int
    END_FIELD_NUMBER: int
    start: Text = ...
    end: Text = ...
    def __init__(self,
        *,
        start : Text = ...,
        end : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end",b"end",u"start",b"start"]) -> None: ...

class TradingSession(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    EXCHANGE_FIELD_NUMBER: int
    TIME_TRADING_FIELD_NUMBER: int
    TIME_AUCTION_FIELD_NUMBER: int
    symbol: Text = ...
    """标的代码"""

    exchange: Text = ...
    """交易所代码"""

    @property
    def time_trading(self) -> RepeatedCompositeFieldContainer[Session]:
        """连续竞价时段"""
        pass
    @property
    def time_auction(self) -> RepeatedCompositeFieldContainer[Session]:
        """集合竞价时段"""
        pass
    def __init__(self,
        *,
        symbol : Text = ...,
        exchange : Text = ...,
        time_trading : Optional[Iterable[Session]] = ...,
        time_auction : Optional[Iterable[Session]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"exchange",b"exchange",u"symbol",b"symbol",u"time_auction",b"time_auction",u"time_trading",b"time_trading"]) -> None: ...

class GetTradingSessionResp(Message):
    DESCRIPTOR: Descriptor = ...
    TRADING_SESSIONS_FIELD_NUMBER: int
    @property
    def trading_sessions(self) -> RepeatedCompositeFieldContainer[TradingSession]: ...
    def __init__(self,
        *,
        trading_sessions : Optional[Iterable[TradingSession]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"trading_sessions",b"trading_sessions"]) -> None: ...

class GetContractExpireRestDaysReq(Message):
    """********************************************************************************
    get_contract_expire_rest_days - 查询合约到期剩余天数
    https://gnuixbiqmy.feishu.cn/docs/doccnom7tXsFsFeYatDxoknFYLc#8woeDc
    *******************************************************************************

    """
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    BY_TRADING_DAYS_FIELD_NUMBER: int
    @property
    def symbols(self) -> RepeatedScalarFieldContainer[Text]:
        """标的代码"""
        pass
    start_date: Text = ...
    """开始时间"""

    end_date: Text = ...
    """结束时间"""

    by_trading_days: bool = ...
    """是否需要按交易日计算"""

    def __init__(self,
        *,
        symbols : Optional[Iterable[Text]] = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        by_trading_days : bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"by_trading_days",b"by_trading_days",u"end_date",b"end_date",u"start_date",b"start_date",u"symbols",b"symbols"]) -> None: ...

class ContractExpireRestDays(Message):
    DESCRIPTOR: Descriptor = ...
    DATE_FIELD_NUMBER: int
    SYMBOL_FIELD_NUMBER: int
    DAYS_TO_EXPIRE_FIELD_NUMBER: int
    date: Text = ...
    """日期 返回字符串即可"""

    symbol: Text = ...
    """标的代码"""

    days_to_expire: Text = ...
    """剩余天数 若不存在则为空字符串"""

    def __init__(self,
        *,
        date : Text = ...,
        symbol : Text = ...,
        days_to_expire : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date",b"date",u"days_to_expire",b"days_to_expire",u"symbol",b"symbol"]) -> None: ...

class GetContractExpireRestDaysResp(Message):
    DESCRIPTOR: Descriptor = ...
    CONTRACT_EXPIRE_REST_DAYS_FIELD_NUMBER: int
    @property
    def contract_expire_rest_days(self) -> RepeatedCompositeFieldContainer[ContractExpireRestDays]: ...
    def __init__(self,
        *,
        contract_expire_rest_days : Optional[Iterable[ContractExpireRestDays]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"contract_expire_rest_days",b"contract_expire_rest_days"]) -> None: ...
