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

class GetConversionPriceReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    DATE_TYPE_FIELD_NUMBER: int
    symbol: Text = ...
    """可转债代码
    参数用法说明:
    必填，只能输入一个可转债的symbol，使用时参考symbol
    """

    start_date: Text = ...
    """开始时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    end_date: Text = ...
    """结束时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    date_type: Text = ...
    """日期类型
    参数用法说明:
    始时间和结束时间的日期类型，
    可选：公告日（默认）、生效日期、执行日期
    默认None表示公告日
    """

    def __init__(self,
        *,
        symbol : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        date_type : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date_type",b"date_type",u"end_date",b"end_date",u"start_date",b"start_date",u"symbol",b"symbol"]) -> None: ...

class ConversionPrice(Message):
    DESCRIPTOR: Descriptor = ...
    PUB_DATE_FIELD_NUMBER: int
    EFFECTIVE_DATE_FIELD_NUMBER: int
    EXECUTION_DATE_FIELD_NUMBER: int
    CONVERSION_PRICE_FIELD_NUMBER: int
    CONVERSION_RATE_FIELD_NUMBER: int
    CONVERSION_VOLUME_FIELD_NUMBER: int
    CONVERSION_AMOUNT_TOTAL_FIELD_NUMBER: int
    BOND_FLOAT_AMOUNT_REMAIN_FIELD_NUMBER: int
    EVENT_TYPE_FIELD_NUMBER: int
    CHANGE_REASON_FIELD_NUMBER: int
    @property
    def pub_date(self) -> Timestamp:
        """公告日期"""
        pass
    @property
    def effective_date(self) -> Timestamp:
        """转股价格生效日期"""
        pass
    @property
    def execution_date(self) -> Timestamp:
        """执行日期"""
        pass
    conversion_price: float = ...
    """转股价格 --单位：元"""

    conversion_rate: float = ...
    """转股比例 --单位：%"""

    conversion_volume: float = ...
    """单位：股"""

    conversion_amount_total: float = ...
    """累计转股金额 --单位：万元，累计转债已经转为股票的金额，累计每次转股金额"""

    bond_float_amount_remain: float = ...
    """债券流通余额 --单位：万元"""

    event_type: Text = ...
    """事件类型  --初始转股价，调整转股价，修正转股价"""

    change_reason: Text = ...
    """转股价变动原因"""

    def __init__(self,
        *,
        pub_date : Optional[Timestamp] = ...,
        effective_date : Optional[Timestamp] = ...,
        execution_date : Optional[Timestamp] = ...,
        conversion_price : float = ...,
        conversion_rate : float = ...,
        conversion_volume : float = ...,
        conversion_amount_total : float = ...,
        bond_float_amount_remain : float = ...,
        event_type : Text = ...,
        change_reason : Text = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"effective_date",b"effective_date",u"execution_date",b"execution_date",u"pub_date",b"pub_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"bond_float_amount_remain",b"bond_float_amount_remain",u"change_reason",b"change_reason",u"conversion_amount_total",b"conversion_amount_total",u"conversion_price",b"conversion_price",u"conversion_rate",b"conversion_rate",u"conversion_volume",b"conversion_volume",u"effective_date",b"effective_date",u"event_type",b"event_type",u"execution_date",b"execution_date",u"pub_date",b"pub_date"]) -> None: ...

class GetConversionPriceRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[ConversionPrice]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[ConversionPrice]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class GetCallInfoReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    DATE_TYPE_FIELD_NUMBER: int
    symbol: Text = ...
    """可转债代码
    参数用法说明:
    必填，只能输入一个可转债，使用时参考symbol
    """

    start_date: Text = ...
    """开始时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    end_date: Text = ...
    """开始时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    date_type: Text = ...
    """日期类型
    参数用法说明:
    开始时间和结束时间的日期类型，
    可选：公告日（默认）、赎回登记日、赎回日
    默认None表示公告日
    """

    def __init__(self,
        *,
        symbol : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        date_type : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date_type",b"date_type",u"end_date",b"end_date",u"start_date",b"start_date",u"symbol",b"symbol"]) -> None: ...

class CallInfo(Message):
    DESCRIPTOR: Descriptor = ...
    PUB_DATE_FIELD_NUMBER: int
    CALL_DATE_FIELD_NUMBER: int
    RECORD_DATE_FIELD_NUMBER: int
    CASH_DATE_FIELD_NUMBER: int
    CALL_TYPE_FIELD_NUMBER: int
    CALL_REASON_FIELD_NUMBER: int
    CALL_PRICE_FIELD_NUMBER: int
    INTEREST_INCLUDED_FIELD_NUMBER: int
    @property
    def pub_date(self) -> Timestamp:
        """公告日 --赎回公告日"""
        pass
    @property
    def call_date(self) -> Timestamp:
        """赎回日 --发行人行权日（实际），公布的赎回日如遇节假日会顺延为非节假日"""
        pass
    @property
    def record_date(self) -> Timestamp:
        """赎回登记日 --理论登记日，非节假日"""
        pass
    @property
    def cash_date(self) -> Timestamp:
        """赎回资金到账日 --投资者赎回款到账日"""
        pass
    call_type: Text = ...
    """赎回类型 --部分赎回，全部赎回"""

    call_reason: Text = ...
    """赎回原因 --1:满足赎回条件，2:强制赎回，3:到期赎回"""

    call_price: float = ...
    """赎回价格 --单位：元/张，每百元面值赎回价格（元），债券面值 加当期应计利息（含税）"""

    interest_included: bool = ...
    """是否包含利息  -- 0:不包含，1:包含"""

    def __init__(self,
        *,
        pub_date : Optional[Timestamp] = ...,
        call_date : Optional[Timestamp] = ...,
        record_date : Optional[Timestamp] = ...,
        cash_date : Optional[Timestamp] = ...,
        call_type : Text = ...,
        call_reason : Text = ...,
        call_price : float = ...,
        interest_included : bool = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"call_date",b"call_date",u"cash_date",b"cash_date",u"pub_date",b"pub_date",u"record_date",b"record_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"call_date",b"call_date",u"call_price",b"call_price",u"call_reason",b"call_reason",u"call_type",b"call_type",u"cash_date",b"cash_date",u"interest_included",b"interest_included",u"pub_date",b"pub_date",u"record_date",b"record_date"]) -> None: ...

class GetCallInfoRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[CallInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[CallInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class GetPutInfoReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    DATE_TYPE_FIELD_NUMBER: int
    symbol: Text = ...
    """可转债代码
    参数用法说明:
    必填，只能输入一个可转债的symbol，使用时参考symbol
    """

    start_date: Text = ...
    """开始时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    end_date: Text = ...
    """结束时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    date_type: Text = ...
    """日期类型
    参数用法说明:
    始时间和结束时间的日期类型，
    可选：公告日（默认）、生效日期、执行日期
    默认None表示公告日
    """

    def __init__(self,
        *,
        symbol : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        date_type : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date_type",b"date_type",u"end_date",b"end_date",u"start_date",b"start_date",u"symbol",b"symbol"]) -> None: ...

class PutInfo(Message):
    DESCRIPTOR: Descriptor = ...
    PUB_DATE_FIELD_NUMBER: int
    PUT_START_DATE_FIELD_NUMBER: int
    PUT_END_DATE_FIELD_NUMBER: int
    CASH_DATE_FIELD_NUMBER: int
    PUT_REASON_FIELD_NUMBER: int
    PUT_PRICE_FIELD_NUMBER: int
    INTEREST_INCLUDED_FIELD_NUMBER: int
    @property
    def pub_date(self) -> Timestamp:
        """公告日 --赎回公告日"""
        pass
    @property
    def put_start_date(self) -> Timestamp:
        """回售起始日 --投资者行权起始日"""
        pass
    @property
    def put_end_date(self) -> Timestamp:
        """回售截止日 --投资者行权截止日"""
        pass
    @property
    def cash_date(self) -> Timestamp:
        """回售资金到账日 --投资者回售款到账日"""
        pass
    put_reason: Text = ...
    """回售原因 --1:满足回售条款，2:满足附加回售条款"""

    put_price: float = ...
    """回售价格 --单位：元/张，每百元面值回售价格（元），债券面值 加当期应计利息（含税）"""

    interest_included: bool = ...
    """是否包含利息  -- 0:不包含，1:包含"""

    def __init__(self,
        *,
        pub_date : Optional[Timestamp] = ...,
        put_start_date : Optional[Timestamp] = ...,
        put_end_date : Optional[Timestamp] = ...,
        cash_date : Optional[Timestamp] = ...,
        put_reason : Text = ...,
        put_price : float = ...,
        interest_included : bool = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"cash_date",b"cash_date",u"pub_date",b"pub_date",u"put_end_date",b"put_end_date",u"put_start_date",b"put_start_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"cash_date",b"cash_date",u"interest_included",b"interest_included",u"pub_date",b"pub_date",u"put_end_date",b"put_end_date",u"put_price",b"put_price",u"put_reason",b"put_reason",u"put_start_date",b"put_start_date"]) -> None: ...

class GetPutInfoRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[PutInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[PutInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class GetAmountChangeReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    DATE_TYPE_FIELD_NUMBER: int
    CHANGE_TYPE_FIELD_NUMBER: int
    symbol: Text = ...
    """可转债代码
    参数用法说明:
    必填，只能输入一个可转债的symbol，使用时参考symbol
    """

    start_date: Text = ...
    """开始时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    end_date: Text = ...
    """结束时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    date_type: Text = ...
    """日期类型
    参数用法说明:
    始时间和结束时间的日期类型，
    可选：公告日（默认）、生效日期、执行日期
    默认None表示公告日
    """

    change_type: int = ...
    """变动类型
    参数用法说明:
    01-首发（默认）
    02-增发
    03-转股
    04-赎回
    05-回售
    06-到期
    默认None表示首发
    """

    def __init__(self,
        *,
        symbol : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        date_type : Text = ...,
        change_type : int = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"change_type",b"change_type",u"date_type",b"date_type",u"end_date",b"end_date",u"start_date",b"start_date",u"symbol",b"symbol"]) -> None: ...

class AmountChange(Message):
    DESCRIPTOR: Descriptor = ...
    PUB_DATE_FIELD_NUMBER: int
    CHANGE_TYPE_FIELD_NUMBER: int
    CHANGE_DATE_FIELD_NUMBER: int
    CHANGE_AMOUNT_FIELD_NUMBER: int
    REMAIN_AMOUNT_FIELD_NUMBER: int
    @property
    def pub_date(self) -> Timestamp:
        """公告日"""
        pass
    change_type: Text = ...
    """变动类型 --首发、增发、转股 、赎回、回售(注销)、到期"""

    @property
    def change_date(self) -> Timestamp:
        """变动日期"""
        pass
    change_amount: float = ...
    """本次变动金额 --单位：万元"""

    remain_amount: float = ...
    """剩余金额 --变动后金额，单位：万元"""

    def __init__(self,
        *,
        pub_date : Optional[Timestamp] = ...,
        change_type : Text = ...,
        change_date : Optional[Timestamp] = ...,
        change_amount : float = ...,
        remain_amount : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"change_date",b"change_date",u"pub_date",b"pub_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"change_amount",b"change_amount",u"change_date",b"change_date",u"change_type",b"change_type",u"pub_date",b"pub_date",u"remain_amount",b"remain_amount"]) -> None: ...

class GetAmountChangeRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[AmountChange]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[AmountChange]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...
