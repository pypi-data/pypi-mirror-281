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
from wifi.cspui.clickh.stations import V, id_head, id_live, stations_table, station_charts


div, span, p, HxEvts = t.div, t.span, t.partial, t.HxEvts

ID = 'stations'  # our namespace base
id = t.id(ID)  # prefixer func
id_tbl = id('stats-tbl')


def div_chart(s=''):
    return div(id('chart'), s, cls='col-lg-12')


def table(cid, ts=None, all_stations=None, live=None):
    r = stations_table.build(
        id_tbl, {'id': cid}, ts=ts, listen=evt_hdlrs, all_stations=all_stations, live=live
    )
    into = r['id'] if live else id('tbl')
    return {
        'div': div(
            into,
            r['table'],
            style='height:300px!important;overflow:scroll;border-bottom:1px solid grey!important;padding-bottom:1em!important;margin-bottom:1em!important',
        ),
        'all_stations': r['all_stations'],
    }


def on_col_click(req):
    col_titl = req['hx'].get('innerText')
    if not col_titl:
        return
    _ = station_charts.build
    return div_chart(_(id('chart'), req['S'].cpe(), col_titl, listen=chart_evt_hdlrs))


def live(subj, spec):
    p = spec['job']['payload']['params']
    dt = p['dt']
    id = p['id']
    return ax_core_ops.rx.interval_immediate(dt).pipe(
        rx.map(lambda _, id=id: usp.state(id))
    )
    # return Rx.merge(
    #    Rx.just(1).pipe(rx.observe_on(GS)), Rx.interval(float(dt / 1000))


API.cpe.live = live  # (our job is searched there)


def stop_live_mode(req):
    cancel = req['S'].subs.pop('live-cpe', 0)
    cancel() if cancel else ''
    return t.css_cls('remove', 'is-live', id_live(id_tbl))


def on_live_mode_tgl(req):
    return stats_table_and_charts(req)
    state = 'is-live' in req['hx']['classList'].values()
    if state:
        return stop_live_mode(req)

    cancel = req['S'].subs.get('live-cpe')
    if cancel:
        return app.info('already listening to live')
    start_live_stream(req)
    return t.css_cls('add', 'is-live', id_live(id_tbl))


def start_live_stream(req):
    h = {'nxt': p(on_live_nxt, req), 'sid': req['S'].id}
    prm = dict(chn='local', dt=3000, id=req['S'].cpe())
    stream = {'action': 'cpe/live', 'params': prm, 'handler': h}
    req['S'].subs['live-cpe'] = hpstreams.listen(stream)


def all_stations(req):
    return getattr(req['S'], 'all_stations', None)


def on_live_nxt(req, msg):
    data = msg['payload']
    if not data:
        app.warn('No result for cpe', id=req['S'].cpe())
        return stop_live_mode(req)
    app.info('have data')
    r = table(req['S'].cpe(), all_stations=all_stations(req), live=data)['div']
    req['S'].send(r)


evt_hdlrs = {
    id_head(id_tbl): ['click', on_col_click, 'innerText'],
    id_live(id_tbl): ['click', on_live_mode_tgl, 'classList'],
}


def on_point_click(req):
    if 'live-cpe' in req['S'].subs:
        stop_live_mode(req)
    ts = req['hx']['local_evt']['x']
    cid = req['S'].cpe()
    return table(cid, int(ts / 1000), all_stations=all_stations(req))['div']


chart_evt_hdlrs = {'point': ['mouseOver', on_point_click]}

rate_col_title = V.rate[0]


def all_charts(req):
    cid = req['S'].cpe()
    _ = station_charts.build
    c = _(id('chart-1'), cid, 'RSSI', listen=chart_evt_hdlrs)
    c += _(id('chart-2'), cid, rate_col_title, listen=chart_evt_hdlrs)
    return div_chart(c)


def stats_table_and_charts(req):
    cid = req['S'].cpe()
    r = table(cid)
    req['S'].all_stations = r['all_stations']
    return div('innerstats', r['div'] + all_charts(req))


t.App.js += [t.src('../js/hc_sync_extremes.js', True)]
t.App.js += [t.src('../js/ctrl_key_listener.js', True)]


class client_stats:
    def on_load(req):
        return div('streaming', stats_table_and_charts(req))

    # def on_vis(req):
    #     app.info('isviz', json=req)
    #
    # def on_invis(req):
    #     return stop_live_mode(req)
    #


HxEvts['streaming'] = client_stats.on_load
# t.add_comp(client_stats)
