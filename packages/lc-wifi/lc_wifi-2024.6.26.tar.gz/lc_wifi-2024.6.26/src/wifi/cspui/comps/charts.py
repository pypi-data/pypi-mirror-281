"""
The frontend of the whole component

Here we set up and handle all browser events to us.

Note that NONE of the called backend utilities gets the request (req) passed(!)
"""

import time
from operators.ctrl.client import API
from operators.ops.tools import Rx, rx, GS
from wifi.cspui.live import usp
from wifi.cspui import tools as t
from devapp.app import app
from operators.con import add_connection
from operators.ctrl import hpstreams
from operators.core import ax_core_ops
from wifi.cspui.clickh.tools import db

div, span, p, HxEvts = t.div, t.span, t.partial, t.HxEvts

ID = 'rad'  # our namespace base
id = t.id(ID)  # prefixer func

i8 = 'toInt8(%s)'
col_defs = [
    ['wifi_2_enabled', i8],
    ['wifi_5_enabled', i8],
    ['wifi_2_autochannel', i8],
    ['wifi_5_autochannel', i8],
]

charts_by_elid = {
    'hxradiocharts': [
        {
            'title': 'Auto Channels',
            'ytitle': 'WiFi and Autochanel Status',
            'cols': [
                'wifi_2_enabled',
                'wifi_5_enabled',
                'wifi_2_autochannel',
                'wifi_5_autochannel',
            ],
        },
        {
            'title': 'Autoasd Channels',
            'ytitle': 'Bar',
            'cols': [
                'wifi_2_enabled',
                'wifi_5_enabled',
                'wifi_2_autochannel',
                'wifi_5_autochannel',
            ],
        },
    ],
    'hxssidcharts': [
        {
            'title': 'Auto Channels',
            'ytitle': 'Foo',
            'cols': [
                'wifi_2_enabled',
                'wifi_5_enabled',
                'wifi_2_autochannel',
                'wifi_5_autochannel',
            ],
        },
    ],
}


def col(c):
    return [c, '%s'] if isinstance(c, str) else c


cols = [col(c) for c in col_defs]
nr_cols = len(cols)
query_cols = ', '.join([c[1] % c[0] for c in cols])

# hours = div('btn-hour', 'hour', hx_trigger='click')
# day = div('btn-day', 'day', hx_trigger='click')
# week = div('btn-week', 'week', hx_trigger='click')
# month = div('btn-month', 'month', hx_trigger='click')
#
# time_sel_buttons = div('time-sel_btns', hours + day + week + month)
time_sel_buttons = div('time-sel_btns', '')


def hour(req):
    return div('btn-day', 'foo')


HxEvts['btn-hour'] = hour


def pretty(s):
    return s.replace('_', ' ').title().replace('Wifi', 'WiFi')


class charts:
    t_kpi_chart = t.js_tmpl('../js/highcharts_kpi.js', True)

    @classmethod
    def build(cls, cpeid, ts_from=None, listen=None):
        ts_from = ts_from or (time.time() - one_week)
        vals = db.all_radio_kpi(cpeid, query_cols, ts_from)
        # Data = dict((n, []) for n in cols)
        singles = [[] for _ in cols]
        Vals = dict((cols[i][0], singles[i]) for i in range(nr_cols))
        for row in vals:
            ts = row[0]
            [singles[i].append([ts, row[i + 1]]) for i in range(nr_cols)]
        ret = []
        idnr = 0
        for elid, charts in charts_by_elid.items():
            sect = []
            for ch in charts:
                ccols = ch['cols']
                L = range(len(ccols))
                data = [{'name': pretty(ccols[i]), 'data': Vals[ccols[i]]} for i in L]
                title = ch['title']
                idc = id(f'chart-{idnr}')
                idnr += 1

                c = t.render(
                    cls.t_kpi_chart,
                    id=idc,
                    title=title,
                    point_evts='{}',
                    y_title=ch['ytitle'],
                    data=data,
                    ts_oldest=1000 * ts_from,
                    ts_newest=1000 * int(time.time()),
                )
                sect.append(div(idc, t.script('', c), cls='col-lg-6'))
            charts = t.lsjoin(sect)
            ret.append(div(elid, time_sel_buttons + charts))
        app.info('Delivering all clickh charts', cpeid=cpeid)
        return t.lsjoin(ret)


def on_point_click(req):
    return  # no click handling here
    # if 'live-cpe' in req['S'].subs:
    #     stop_live_mode(req)
    # ts = req['hx']['local_evt']['x']
    # cid = req['S'].cpe()
    # return table(cid, int(ts / 1000))


chart_evt_hdlrs = {'point': ['mouseOver', on_point_click]}

rate_col_title = 'title'


# def div_charts(s=''):
#     return div(id('charts'), s, cls='col-lg-12')


t.App.js += [t.src('../js/hc_sync_extremes.js', True)]


class all_charts:
    def on_load(req):
        cpeid = req['S'].cpe()
        return charts.build(cpeid)


HxEvts['hxcharts'] = all_charts.on_load


one_week = 7 * 86400
