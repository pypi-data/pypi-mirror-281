from ks_trade_api.constant import *
from vnpy.trader.object import *
from dataclasses import dataclass, field
from datetime import datetime
import re
from typing import Union
from decimal import Decimal
from typing import Optional

@dataclass
class MyBookData(BaseData):
    symbol: str
    exchange: Exchange
    datetime: datetime
    localtime: datetime = None
    name: str = ""

    bid_price_1: Decimal = Decimal('0')
    bid_price_2: Decimal = Decimal('0')
    bid_price_3: Decimal = Decimal('0')
    bid_price_4: Decimal = Decimal('0')
    bid_price_5: Decimal = Decimal('0')

    ask_price_1: Decimal = Decimal('0')
    ask_price_2: Decimal = Decimal('0')
    ask_price_3: Decimal = Decimal('0')
    ask_price_4: Decimal = Decimal('0')
    ask_price_5: Decimal = Decimal('0')

    bid_volume_1: Decimal = Decimal('0')
    bid_volume_2: Decimal = Decimal('0')
    bid_volume_3: Decimal = Decimal('0')
    bid_volume_4: Decimal = Decimal('0')
    bid_volume_5: Decimal = Decimal('0')

    ask_volume_1: Decimal = Decimal('0')
    ask_volume_2: Decimal = Decimal('0')
    ask_volume_3: Decimal = Decimal('0')
    ask_volume_4: Decimal = Decimal('0')
    ask_volume_5: Decimal = Decimal('0')

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"

@dataclass
class MyTickData(MyBookData):
    volume: Decimal = Decimal('0')
    turnover: Decimal = Decimal('0')
    open_interest: Decimal = Decimal('0')
    last_price: Decimal = Decimal('0')
    last_volume: Decimal = Decimal('0')
    limit_up: Decimal = Decimal('0')
    limit_down: Decimal = Decimal('0')
    open_price: Decimal = Decimal('0')
    high_price: Decimal = Decimal('0')
    low_price: Decimal = Decimal('0')
    pre_close: Decimal = Decimal('0')

    settlement_price: float = 0
    pre_settlement_price: float = 0

@dataclass
class MyRawTickData(BaseData):
    symbol: str
    exchange: Exchange
    datetime: datetime
    localtime: datetime = None
    name: str = ""
    
    volume: Decimal = Decimal('0')
    turnover: Decimal = Decimal('0')
    open_interest: Decimal = Decimal('0')
    last_price: Decimal = Decimal('0')
    last_volume: Decimal = Decimal('0')
    limit_up: Decimal = Decimal('0')
    limit_down: Decimal = Decimal('0')
    open_price: Decimal = Decimal('0')
    high_price: Decimal = Decimal('0')
    low_price: Decimal = Decimal('0')
    pre_close: Decimal = Decimal('0')

    settlement_price: float = 0
    pre_settlement_price: float = 0

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"

@dataclass
class MyOrderData(OrderData):
    # todo 增加
    # frozen_margin: float = 0
    # frozen_commission: float = 0

    price: Decimal = Decimal('0')
    volume: Decimal = Decimal('0')
    traded: Decimal = Decimal('0')


    error: str = ''
    order_sys_id: str = ''
    profit_price: Union[Decimal, None] = None # My.add 止盈价
    loss_price: Union[Decimal, None] = None # My.add 止损价
    positionids: list[str] = field(default_factory=list)
    
    
    def __post_init__(self) -> None:
        """"""
        self.exchange: Exchange = EXCHANGE_MAP[self.exchange] if type(self.exchange) is str else self.exchange
        self.type: OrderType = ORDER_TYPE_MAP[self.type] if type(self.type) is str else self.type
        self.direction: Direction = DIRECTION_MAP[self.direction] if type(self.direction) is str else self.direction
        self.offset: Offset = OFFSET_MAP[self.offset] if type(self.offset) is str else self.offset
        self.status: Offset = STATUS_MAP[self.status] if type(self.status) is str else self.status
        self.vt_positionids: list[str] = [f"{self.gateway_name}.{x}" for x in self.positionids]
        if isinstance(self.datetime, str):
            self.datetime: datetime = datetime.strptime(self.datetime, DATETIME_FMT) if self.datetime else ''
        if self.datetime is None:
            self.datetime = datetime.now().replace(tzinfo=CHINA_TZ)

        super().__post_init__()

@dataclass
class MyTradeData(TradeData):
    price: Decimal = Decimal('0')
    volume: Decimal = Decimal('0')

    position_price: Decimal = Decimal('0')
    positionid: str = ''

    def __post_init__(self) -> None:
        """"""
        self.exchange: Exchange = EXCHANGE_MAP[self.exchange]
        self.direction: Direction = DIRECTION_MAP[self.direction]
        self.offset: Offset = OFFSET_MAP[self.offset]
        if isinstance(self.datetime, str):
            self.datetime: datetime = datetime.strptime(self.datetime, DATETIME_FMT)
        # 先要获取exchange的enum，才能拼接vt_symbol
        super().__post_init__()
        matched = re.search(r'_((\d*-*)+)$', self.positionid)
        self.position_date: str = matched[1] if matched else ''

@dataclass
class MyPositionData(BaseData):
    """
    Trade data contains information of a fill of an order. One order
    can have several trade fills.
    """

    symbol: str
    exchange: Exchange
    direction: Direction = None

    pnl: float = 0
    yd_volume: Decimal = Decimal('0')

    price: Decimal = Decimal('0')
    volume: Decimal = Decimal('0')
    frozen: Decimal = Decimal('0')
    orderids: list[str] = field(default_factory=list)
    available: Decimal = Decimal('0')
    margin: float = 0
    profit: float = 0 # 持仓盈亏
    settle_profit: float = 0 # 盯市盈亏
    date: str = ''
    profit_price: Union[float, None] = None # My.add 止盈价
    loss_price: Union[float, None] = None # My.add 止损价

    def __post_init__(self) -> None:
        """"""
        self.exchange: Exchange = EXCHANGE_MAP[self.exchange]
        self.direction: Direction = DIRECTION_MAP[self.direction]
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"
        self.vt_orderids: list[str] = [f"{self.gateway_name}.{x}" for x in self.orderids]
        self.positionid: str = f"{self.symbol}_{self.direction.name}_{self.date}"
        if self.volume > 0:
            self.available: float = self.volume - self.frozen
        else:
            self.available: float = self.volume + self.frozen
        self.vt_positionid: str = f"{self.gateway_name}.{self.positionid}"


@dataclass
class MyMarginRateData(BaseData):
    """
    保证金费率
    """

    symbol: str
    exchange: Exchange
    
    long_margin_ratio_by_money: float = 0
    long_margin_ratio_by_volume: float = 0
    short_margin_ratio_by_money: float = 0
    short_margin_ratio_by_volume: float = 0

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"

@dataclass
class MyCommissionRateData(BaseData):
    """
    手续费率
    """

    symbol: str
    exchange: Exchange
    
    open_ratio_by_money: float = 0
    open_ratio_by_volume: float = 0
    close_ratio_by_money: float = 0
    close_ratio_by_volume: float = 0
    close_today_ratio_by_money: float = 0
    close_today_ratio_by_volume: float = 0

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"

@dataclass
class MyOptionInstrTradeCost(BaseData):
    """
    保证金费率
    """

    symbol: str
    exchange: Exchange
    
    fixed_margin: float = 0
    mini_margin: float = 0

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"

@dataclass
class MyPushData(BaseData):
    """
    Log data is used for recording log messages on GUI or in log files.
    """

    msg: str = ''
    title: str = ''
    is_at_all: bool = True
    dd_index: int = 0 # 第几个钉钉，默认第一个

@dataclass
class MyZmqData(BaseData):
    """
    Log data is used for recording log messages on GUI or in log files.
    """
    topic: str = ''
    msg: str = ''

@dataclass
class MyOrderRequest(OrderRequest):
    time_in_force: TimeInForce = TimeInForce.GTC
    profit_price: Union[float, None] = None, # My.add 止盈价
    loss_price: Union[float, None] = None, # My.add 止损价
    
    def create_order_data(self, orderid: str, gateway_name: str) -> OrderData:
        """
        Create order data from request.
        """
        order: MyOrderData = MyOrderData(
            symbol=self.symbol,
            exchange=self.exchange,
            orderid=orderid,
            type=self.type,
            direction=self.direction,
            offset=self.offset,
            price=self.price,
            volume=self.volume,
            reference=self.reference,
            profit_price=self.profit_price,
            loss_price=self.loss_price,
            gateway_name=gateway_name
        )
        return order
    
@dataclass
class MySubscribeRequest(SubscribeRequest):
    types: list[SubscribeType] = field(default_factory=list)

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}" if self.exchange else ''

@dataclass
class MyAccountData(AccountData):
    """
    Account data contains information about balance, frozen and
    available.
    """

    currency: Currency = Currency.CNY

@dataclass
class MyErrorData(BaseData):
    """
    Tick data contains information about:
        * last trade in market
        * orderbook snapshot
        * intraday market statistics.
    """

    code: Optional[ErrorCode] = None
    msg: Optional[str] = None
    method: Optional[str] = None
    args: Optional[str] = None
    kvargs: Optional[dict] = None
    traceback: Optional[str] = None

    
