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

class GetEtfConstituentsReq(Message):
    DESCRIPTOR: Descriptor = ...
    ETF_FIELD_NUMBER: int
    etf: Text = ...
    """ETF代码
    参数用法说明:
    必填，只能输入一个ETF的symbol，如：SHSE.510050
    """

    def __init__(self,
        *,
        etf : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"etf",b"etf"]) -> None: ...

class EtfConstituents(Message):
    DESCRIPTOR: Descriptor = ...
    ETF_FIELD_NUMBER: int
    ETF_NAME_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    SYMBOL_FIELD_NUMBER: int
    AMOUNT_FIELD_NUMBER: int
    CASH_SUBS_TYPE_FIELD_NUMBER: int
    CASH_SUBS_SUM_FIELD_NUMBER: int
    CASH_PREMIUM_RATE_FIELD_NUMBER: int
    etf: Text = ...
    """ETF代码"""

    etf_name: Text = ...
    """ETF名称"""

    @property
    def trade_date(self) -> Timestamp:
        """交易日期"""
        pass
    symbol: Text = ...
    """成分股代码"""

    amount: float = ...
    """股票数量"""

    cash_subs_type: Text = ...
    """现金替代标志"""

    cash_subs_sum: float = ...
    """固定替代金额"""

    cash_premium_rate: float = ...
    """现金替代溢价比例 --单位：%"""

    def __init__(self,
        *,
        etf : Text = ...,
        etf_name : Text = ...,
        trade_date : Optional[Timestamp] = ...,
        symbol : Text = ...,
        amount : float = ...,
        cash_subs_type : Text = ...,
        cash_subs_sum : float = ...,
        cash_premium_rate : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"amount",b"amount",u"cash_premium_rate",b"cash_premium_rate",u"cash_subs_sum",b"cash_subs_sum",u"cash_subs_type",b"cash_subs_type",u"etf",b"etf",u"etf_name",b"etf_name",u"symbol",b"symbol",u"trade_date",b"trade_date"]) -> None: ...

class GetEtfConstituentsRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[EtfConstituents]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[EtfConstituents]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class GetPortfolioReq(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    REPORT_TYPE_FIELD_NUMBER: int
    PORTFOLIO_TYPE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码
    参数用法说明:
    必填，只能输入一个基金的symbol，如：SZSE.161133
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

    report_type: int = ...
    """报表类别
    参数用法说明:
    公布持仓所在的报表类别，必填，可选：
    10:一季报
    20:中报
    30:三季报
    40:年报
    50:二季报
    60:四季报
    """

    portfolio_type: Text = ...
    """投资组合类型
    stk: 股票投资组合
    bnd: 债券投资组合
    fnd: 基金投资组合
    """

    def __init__(self,
        *,
        fund : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        report_type : int = ...,
        portfolio_type : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_date",b"end_date",u"fund",b"fund",u"portfolio_type",b"portfolio_type",u"report_type",b"report_type",u"start_date",b"start_date"]) -> None: ...

class PortfolioStockInfo(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    FUND_NAME_FIELD_NUMBER: int
    PUB_DATE_FIELD_NUMBER: int
    PERIOD_END_FIELD_NUMBER: int
    SYMBOL_FIELD_NUMBER: int
    SEC_NAME_FIELD_NUMBER: int
    HOLD_SHARE_FIELD_NUMBER: int
    HOLD_VALUE_FIELD_NUMBER: int
    NV_RATE_FIELD_NUMBER: int
    TTL_SHARE_RATE_FIELD_NUMBER: int
    CIRC_SHARE_RATE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码  --查询资产组合的基金代码"""

    fund_name: Text = ...
    """基金名称"""

    @property
    def pub_date(self) -> Timestamp:
        """公告日期  --在指定时间段[开始时间,结束时间]内的公告日期"""
        pass
    @property
    def period_end(self) -> Timestamp:
        """报告期 -- 持仓截止日期"""
        pass
    symbol: Text = ...
    """股票代码"""

    sec_name: Text = ...
    """股票名称"""

    hold_share: float = ...
    """持仓股数"""

    hold_value: float = ...
    """持仓市值"""

    nv_rate: float = ...
    """占净值比例  --单位：%"""

    ttl_share_rate: float = ...
    """占总股本比例 --单位：%"""

    circ_share_rate: float = ...
    """占流通股比例 --单位：%s"""

    def __init__(self,
        *,
        fund : Text = ...,
        fund_name : Text = ...,
        pub_date : Optional[Timestamp] = ...,
        period_end : Optional[Timestamp] = ...,
        symbol : Text = ...,
        sec_name : Text = ...,
        hold_share : float = ...,
        hold_value : float = ...,
        nv_rate : float = ...,
        ttl_share_rate : float = ...,
        circ_share_rate : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"period_end",b"period_end",u"pub_date",b"pub_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"circ_share_rate",b"circ_share_rate",u"fund",b"fund",u"fund_name",b"fund_name",u"hold_share",b"hold_share",u"hold_value",b"hold_value",u"nv_rate",b"nv_rate",u"period_end",b"period_end",u"pub_date",b"pub_date",u"sec_name",b"sec_name",u"symbol",b"symbol",u"ttl_share_rate",b"ttl_share_rate"]) -> None: ...

class PortfolioBondInfo(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    FUND_NAME_FIELD_NUMBER: int
    PUB_DATE_FIELD_NUMBER: int
    PERIOD_END_FIELD_NUMBER: int
    SYMBOL_FIELD_NUMBER: int
    SEC_NAME_FIELD_NUMBER: int
    HOLD_SHARE_FIELD_NUMBER: int
    HOLD_VALUE_FIELD_NUMBER: int
    NV_RATE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码  --查询资产组合的基金代码"""

    fund_name: Text = ...
    """基金名称"""

    @property
    def pub_date(self) -> Timestamp:
        """公告日期  --在指定时间段[开始时间,结束时间]内的公告日期"""
        pass
    @property
    def period_end(self) -> Timestamp:
        """报告期 -- 持仓截止日期"""
        pass
    symbol: Text = ...
    """债券代码"""

    sec_name: Text = ...
    """债券名称"""

    hold_share: float = ...
    """持仓数量"""

    hold_value: float = ...
    """持仓市值"""

    nv_rate: float = ...
    """占净值比例 --单位：%"""

    def __init__(self,
        *,
        fund : Text = ...,
        fund_name : Text = ...,
        pub_date : Optional[Timestamp] = ...,
        period_end : Optional[Timestamp] = ...,
        symbol : Text = ...,
        sec_name : Text = ...,
        hold_share : float = ...,
        hold_value : float = ...,
        nv_rate : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"period_end",b"period_end",u"pub_date",b"pub_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"fund",b"fund",u"fund_name",b"fund_name",u"hold_share",b"hold_share",u"hold_value",b"hold_value",u"nv_rate",b"nv_rate",u"period_end",b"period_end",u"pub_date",b"pub_date",u"sec_name",b"sec_name",u"symbol",b"symbol"]) -> None: ...

class PortfolioFundInfo(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    FUND_NAME_FIELD_NUMBER: int
    PUB_DATE_FIELD_NUMBER: int
    PERIOD_END_FIELD_NUMBER: int
    SYMBOL_FIELD_NUMBER: int
    SEC_NAME_FIELD_NUMBER: int
    HOLD_SHARE_FIELD_NUMBER: int
    HOLD_VALUE_FIELD_NUMBER: int
    NV_RATE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码  --查询资产组合的基金代码"""

    fund_name: Text = ...
    """基金名称"""

    @property
    def pub_date(self) -> Timestamp:
        """公告日期  --在指定时间段[开始时间,结束时间]内的公告日期"""
        pass
    @property
    def period_end(self) -> Timestamp:
        """报告期 -- 持仓截止日期"""
        pass
    symbol: Text = ...
    """基金代码"""

    sec_name: Text = ...
    """基金名称"""

    hold_share: float = ...
    """持有份额"""

    hold_value: float = ...
    """期末市值"""

    nv_rate: float = ...
    """占净值比例 --单位：%"""

    def __init__(self,
        *,
        fund : Text = ...,
        fund_name : Text = ...,
        pub_date : Optional[Timestamp] = ...,
        period_end : Optional[Timestamp] = ...,
        symbol : Text = ...,
        sec_name : Text = ...,
        hold_share : float = ...,
        hold_value : float = ...,
        nv_rate : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"period_end",b"period_end",u"pub_date",b"pub_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"fund",b"fund",u"fund_name",b"fund_name",u"hold_share",b"hold_share",u"hold_value",b"hold_value",u"nv_rate",b"nv_rate",u"period_end",b"period_end",u"pub_date",b"pub_date",u"sec_name",b"sec_name",u"symbol",b"symbol"]) -> None: ...

class GetPortfolioRsp(Message):
    """portfolio_stock, portfolio_bond, portfolio_fund 只有一个有值, 根据选择的投资组合类型填充数据"""
    DESCRIPTOR: Descriptor = ...
    PORTFOLIO_STOCK_FIELD_NUMBER: int
    PORTFOLIO_BOND_FIELD_NUMBER: int
    PORTFOLIO_FUND_FIELD_NUMBER: int
    @property
    def portfolio_stock(self) -> RepeatedCompositeFieldContainer[PortfolioStockInfo]:
        """股票投资组合  --基金持有的股票信息"""
        pass
    @property
    def portfolio_bond(self) -> RepeatedCompositeFieldContainer[PortfolioBondInfo]:
        """债券投资组合  --基金持有的债券信息"""
        pass
    @property
    def portfolio_fund(self) -> RepeatedCompositeFieldContainer[PortfolioFundInfo]:
        """基金投资组合  --基金持有的基金信息"""
        pass
    def __init__(self,
        *,
        portfolio_stock : Optional[Iterable[PortfolioStockInfo]] = ...,
        portfolio_bond : Optional[Iterable[PortfolioBondInfo]] = ...,
        portfolio_fund : Optional[Iterable[PortfolioFundInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"portfolio_bond",b"portfolio_bond",u"portfolio_fund",b"portfolio_fund",u"portfolio_stock",b"portfolio_stock"]) -> None: ...

class GetNetValueReq(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码
    参数用法说明:
    必填，只能输入一个基金的symbol，如：SZSE.159919
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

    def __init__(self,
        *,
        fund : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_date",b"end_date",u"fund",b"fund",u"start_date",b"start_date"]) -> None: ...

class NetValueInfo(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    UNIT_NV_FIELD_NUMBER: int
    UNIT_NV_ACCU_FIELD_NUMBER: int
    UNIT_NV_ADJ_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码  --查询净值的基金代码"""

    @property
    def trade_date(self) -> Timestamp:
        """交易日期"""
        pass
    unit_nv: float = ...
    """单位净值  --T日单位净值是每个基金份额截至T日的净值（也是申赎的价格）"""

    unit_nv_accu: float = ...
    """累计单位净值  --T日累计净值是指，在基金成立之初投资该基金1元钱，在现金分红方式下，截至T日账户的净值"""

    unit_nv_adj: float = ...
    """复权单位净值  --T日复权净值是指，在基金成立之初投资该基金1元钱，在分红再投资方式下，截至T日账户的净值"""

    def __init__(self,
        *,
        fund : Text = ...,
        trade_date : Optional[Timestamp] = ...,
        unit_nv : float = ...,
        unit_nv_accu : float = ...,
        unit_nv_adj : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"fund",b"fund",u"trade_date",b"trade_date",u"unit_nv",b"unit_nv",u"unit_nv_accu",b"unit_nv_accu",u"unit_nv_adj",b"unit_nv_adj"]) -> None: ...

class GetNetValueRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[NetValueInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[NetValueInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class FndGetAdjFactorReq(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    BASE_DATE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码
    参数用法说明:
    必填，只能输入一个基金的symbol，如：SZSE.159919
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

    base_date: Text = ...
    """复权基准日
    参数用法说明:
    前复权的基准日，默认为结束时间，%Y-%m-%d 格式，
    默认None表示最新时间
    """

    def __init__(self,
        *,
        fund : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        base_date : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"base_date",b"base_date",u"end_date",b"end_date",u"fund",b"fund",u"start_date",b"start_date"]) -> None: ...

class FndAdjFactorInfo(Message):
    DESCRIPTOR: Descriptor = ...
    TRADE_DATE_FIELD_NUMBER: int
    ADJ_FACTOR_BWD_ACC_FIELD_NUMBER: int
    ADJ_FACTOR_FWD_FIELD_NUMBER: int
    @property
    def trade_date(self) -> Timestamp:
        """交易日期    --最新交易日的日期"""
        pass
    adj_factor_bwd_acc: float = ...
    """当日累计后复权因子  --T日累计后复权因子=T日后复权因子*T-1日累计后复权因子（第一个累计后复权因子=第一个后复权因子）"""

    adj_factor_fwd: float = ...
    """当日前复权因子   --T日前复权因子=T日后复权因子/复权基准日后复权因子"""

    def __init__(self,
        *,
        trade_date : Optional[Timestamp] = ...,
        adj_factor_bwd_acc : float = ...,
        adj_factor_fwd : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"adj_factor_bwd_acc",b"adj_factor_bwd_acc",u"adj_factor_fwd",b"adj_factor_fwd",u"trade_date",b"trade_date"]) -> None: ...

class FndGetAdjFactorRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[FndAdjFactorInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[FndAdjFactorInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class FndGetDividendReq(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    DATE_TYPE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码
    参数用法说明:
    必填，只能输入一个基金的symbol，如：SZSE.159919
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
    开始时间和结束时间的日期类型，
    可选：公告日（默认）、权益登记日、除息日、红放日
    默认None表示公告日
    """

    def __init__(self,
        *,
        fund : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        date_type : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date_type",b"date_type",u"end_date",b"end_date",u"fund",b"fund",u"start_date",b"start_date"]) -> None: ...

class FndDividendInfo(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    PUB_DATE_FIELD_NUMBER: int
    EVENT_PROGRESS_FIELD_NUMBER: int
    DVD_RATIO_FIELD_NUMBER: int
    DVD_BASE_DATE_FIELD_NUMBER: int
    RT_REG_DATE_FIELD_NUMBER: int
    EX_ACT_DATE_FIELD_NUMBER: int
    EX_DVD_DATE_FIELD_NUMBER: int
    PAY_DVD_DATE_FIELD_NUMBER: int
    TRANS_DVD_DATE_FIELD_NUMBER: int
    REINVEST_CFM_DATE_FIELD_NUMBER: int
    RI_SHR_ARR_DATE_FIELD_NUMBER: int
    RI_SHR_RDM_DATE_FIELD_NUMBER: int
    EARN_DISTR_FIELD_NUMBER: int
    CASH_PAY_FIELD_NUMBER: int
    BASE_UNIT_NV_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码   --查询分红信息的基金代码"""

    @property
    def pub_date(self) -> Timestamp:
        """公告日"""
        pass
    event_progress: Text = ...
    """方案进度"""

    dvd_ratio: float = ...
    """派息比例 --10:X，每10份税前分红"""

    @property
    def dvd_base_date(self) -> Timestamp:
        """分配收益基准日"""
        pass
    @property
    def rt_reg_date(self) -> Timestamp:
        """权益登记日"""
        pass
    @property
    def ex_act_date(self) -> Timestamp:
        """实际除息日"""
        pass
    @property
    def ex_dvd_date(self) -> Timestamp:
        """场内除息日"""
        pass
    @property
    def pay_dvd_date(self) -> Timestamp:
        """场内红利发放日"""
        pass
    @property
    def trans_dvd_date(self) -> Timestamp:
        """场内红利款账户划出日"""
        pass
    @property
    def reinvest_cfm_date(self) -> Timestamp:
        """红利再投资确定日"""
        pass
    @property
    def ri_shr_arr_date(self) -> Timestamp:
        """红利再投资份额到账日"""
        pass
    @property
    def ri_shr_rdm_date(self) -> Timestamp:
        """红利再投资赎回起始日"""
        pass
    earn_distr: float = ...
    """可分配收益 --单位：元"""

    cash_pay: float = ...
    """本期实际红利发放 --单位：元"""

    base_unit_nv: float = ...
    """基准日基金份额净值"""

    def __init__(self,
        *,
        fund : Text = ...,
        pub_date : Optional[Timestamp] = ...,
        event_progress : Text = ...,
        dvd_ratio : float = ...,
        dvd_base_date : Optional[Timestamp] = ...,
        rt_reg_date : Optional[Timestamp] = ...,
        ex_act_date : Optional[Timestamp] = ...,
        ex_dvd_date : Optional[Timestamp] = ...,
        pay_dvd_date : Optional[Timestamp] = ...,
        trans_dvd_date : Optional[Timestamp] = ...,
        reinvest_cfm_date : Optional[Timestamp] = ...,
        ri_shr_arr_date : Optional[Timestamp] = ...,
        ri_shr_rdm_date : Optional[Timestamp] = ...,
        earn_distr : float = ...,
        cash_pay : float = ...,
        base_unit_nv : float = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"dvd_base_date",b"dvd_base_date",u"ex_act_date",b"ex_act_date",u"ex_dvd_date",b"ex_dvd_date",u"pay_dvd_date",b"pay_dvd_date",u"pub_date",b"pub_date",u"reinvest_cfm_date",b"reinvest_cfm_date",u"ri_shr_arr_date",b"ri_shr_arr_date",u"ri_shr_rdm_date",b"ri_shr_rdm_date",u"rt_reg_date",b"rt_reg_date",u"trans_dvd_date",b"trans_dvd_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"base_unit_nv",b"base_unit_nv",u"cash_pay",b"cash_pay",u"dvd_base_date",b"dvd_base_date",u"dvd_ratio",b"dvd_ratio",u"earn_distr",b"earn_distr",u"event_progress",b"event_progress",u"ex_act_date",b"ex_act_date",u"ex_dvd_date",b"ex_dvd_date",u"fund",b"fund",u"pay_dvd_date",b"pay_dvd_date",u"pub_date",b"pub_date",u"reinvest_cfm_date",b"reinvest_cfm_date",u"ri_shr_arr_date",b"ri_shr_arr_date",u"ri_shr_rdm_date",b"ri_shr_rdm_date",u"rt_reg_date",b"rt_reg_date",u"trans_dvd_date",b"trans_dvd_date"]) -> None: ...

class FndGetDividendRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[FndDividendInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[FndDividendInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class GetSplitReq(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    DATE_TYPE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码
    参数用法说明:
    必填，只能输入一个基金的symbol，如：SZSE.159919
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
    开始时间和结束时间的日期类型，
    可选：公告日（默认）、权益登记日、除息日、红放日
    默认None表示公告日
    """

    def __init__(self,
        *,
        fund : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        date_type : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"date_type",b"date_type",u"end_date",b"end_date",u"fund",b"fund",u"start_date",b"start_date"]) -> None: ...

class SplitInfo(Message):
    DESCRIPTOR: Descriptor = ...
    FUND_FIELD_NUMBER: int
    PUB_DATE_FIELD_NUMBER: int
    SPLIT_TYPE_FIELD_NUMBER: int
    SPLIT_RATIO_FIELD_NUMBER: int
    BASE_DATE_FIELD_NUMBER: int
    EX_DATE_FIELD_NUMBER: int
    SHARE_CHANGE_REG_DATE_FIELD_NUMBER: int
    NV_SPLIT_PUB_DATE_FIELD_NUMBER: int
    RT_REG_DATE_FIELD_NUMBER: int
    EX_DATE_CLOSE_FIELD_NUMBER: int
    fund: Text = ...
    """基金代码"""

    @property
    def pub_date(self) -> Timestamp:
        """公告日"""
        pass
    split_type: Text = ...
    """拆分折算类型"""

    split_ratio: float = ...
    """拆分折算比例"""

    @property
    def base_date(self) -> Timestamp:
        """拆分折算基准日"""
        pass
    @property
    def ex_date(self) -> Timestamp:
        """拆分折算场内除权日"""
        pass
    @property
    def share_change_reg_date(self) -> Timestamp:
        """基金份额变更登记日"""
        pass
    @property
    def nv_split_pub_date(self) -> Timestamp:
        """基金披露净值拆分折算日"""
        pass
    @property
    def rt_reg_date(self) -> Timestamp:
        """权益登记日"""
        pass
    @property
    def ex_date_close(self) -> Timestamp:
        """场内除权日(收盘价)"""
        pass
    def __init__(self,
        *,
        fund : Text = ...,
        pub_date : Optional[Timestamp] = ...,
        split_type : Text = ...,
        split_ratio : float = ...,
        base_date : Optional[Timestamp] = ...,
        ex_date : Optional[Timestamp] = ...,
        share_change_reg_date : Optional[Timestamp] = ...,
        nv_split_pub_date : Optional[Timestamp] = ...,
        rt_reg_date : Optional[Timestamp] = ...,
        ex_date_close : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"base_date",b"base_date",u"ex_date",b"ex_date",u"ex_date_close",b"ex_date_close",u"nv_split_pub_date",b"nv_split_pub_date",u"pub_date",b"pub_date",u"rt_reg_date",b"rt_reg_date",u"share_change_reg_date",b"share_change_reg_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"base_date",b"base_date",u"ex_date",b"ex_date",u"ex_date_close",b"ex_date_close",u"fund",b"fund",u"nv_split_pub_date",b"nv_split_pub_date",u"pub_date",b"pub_date",u"rt_reg_date",b"rt_reg_date",u"share_change_reg_date",b"share_change_reg_date",u"split_ratio",b"split_ratio",u"split_type",b"split_type"]) -> None: ...

class GetSplitRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[SplitInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[SplitInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...
