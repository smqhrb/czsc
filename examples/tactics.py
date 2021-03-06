# -*- coding: utf-8 -*-
"""
author: zengbin93
email: zeng_bin8888@163.com
create_dt: 2022/2/10 21:12
"""
from czsc import signals, CZSC
from czsc.objects import Freq, Operate, Signal, Factor, Event
from collections import OrderedDict


def trader_strategy_a():
    """A股市场择时策略A"""
    def get_signals(c: CZSC) -> OrderedDict:
        s = OrderedDict({"symbol": c.symbol, "dt": c.bars_raw[-1].dt, "close": c.bars_raw[-1].close})
        if c.freq in [Freq.F15]:
            s.update(signals.bxt.get_s_d0_bi(c))
            s.update(signals.other.get_s_zdt(c, di=1))
            s.update(signals.other.get_s_op_time_span(c, op='开多', time_span=('13:00', '14:50')))
            s.update(signals.other.get_s_op_time_span(c, op='平多', time_span=('09:35', '14:50')))

        if c.freq in [Freq.F60, Freq.D, Freq.W]:
            s.update(signals.ta.get_s_macd(c, di=1))
        return s

    long_states_pos = {
        'hold_long_a': 1.0,
        'hold_long_b': 1.0,
        'hold_long_c': 1.0,
    }

    short_states_pos = None

    long_events = [
        Event(name="开多", operate=Operate.LO, factors=[
            Factor(name="低吸", signals_all=[
                Signal("开多时间范围_13:00_14:50_是_任意_任意_0"),
                Signal("15分钟_倒1K_ZDT_非涨跌停_任意_任意_0"),
                Signal("60分钟_倒1K_MACD多空_多头_任意_任意_0"),
                Signal("15分钟_倒0笔_方向_向上_任意_任意_0"),
                Signal("15分钟_倒0笔_长度_5根K线以下_任意_任意_0"),
            ]),
        ]),

        Event(name="平多", operate=Operate.LE, factors=[
            Factor(name="持有资金", signals_all=[
                Signal("平多时间范围_09:35_14:50_是_任意_任意_0"),
                Signal("15分钟_倒1K_ZDT_非涨跌停_任意_任意_0"),
            ], signals_not=[
                Signal("15分钟_倒0笔_方向_向上_任意_任意_0"),
                Signal("60分钟_倒1K_MACD多空_多头_任意_任意_0"),
            ]),
        ]),
    ]

    short_events = None

    tactic = {
        "base_freq": '15分钟',
        "freqs": ['60分钟', '日线'],
        "get_signals": get_signals,
        "signals_n": 0,

        "long_states_pos": long_states_pos,
        "long_events": long_events,
        "long_min_interval": 3600*4,

        "short_states_pos": short_states_pos,
        "short_events": short_events,
        "short_min_interval": 3600*4,
    }

    return tactic
