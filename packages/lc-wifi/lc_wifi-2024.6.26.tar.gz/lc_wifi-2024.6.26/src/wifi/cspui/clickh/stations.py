"""
Delivering Table and Charts for the Stations Overview
"""


import datetime
from wifi.cspui.const import HxEvts, App
from wifi.cspui.tools import thead, trs, lsjoin, js_tmpl, render, script, div, span
from wifi.cspui.clickh import html
from wifi.cspui.clickh.tools import (
    formatters,
    concat,
    is_vcol,
    ch_getter,
    ch_getters,
    title,
)
from wifi.cspui.clickh.tools import live_hosts, fmt, db
from wifi.cspui.clickh.tables import Hosts as H
import time


class V:
    """Virtual Columns"""

    rate = ['RX TX Mb/s', concat([H.LastDataDownlinkRate, H.LastDataUplinkRate], ' / ')]
    bytes = ['kB', concat([H.BytesReceived, H.BytesSent], ' / ')]
    errs = ['Errors', concat([H.ErrorsReceived, H.ErrorsSent], ' / ')]
    pkts = ['Pkts', concat([H.PacketsReceived, H.PacketsSent], ' / ')]
    link = ['Link', concat([H.InterfaceType, H.standard], ' '), fmt.link]


def id_head(id):
    return id + '-head'


def id_live(id):
    return id + '-live'


class stations_table:
    App.css.append(html.style)
    cols = [
        H.HostName,
        H.vendor,
        H.PhysAddress,
        H.IPAddress,
        V.link,
        H.SignalStrength,
        V.rate,
        H.band,
        H.ssid,
        H.SNR,
        V.errs,
        V.bytes,
        V.pkts,
        H.Retransmissions,
        H.RetransCount,
    ]
    fmts = formatters(cols)
    ch_cols = ch_getters(cols)
    hdr_cols = '\n'.join([f'<th>{title(c)}</th>' for c in cols])
    head_row = html.t_head % hdr_cols

    @classmethod
    def apply_formatters(cls, rows, all_stations):
        pacol = cls.cols.index(H.PhysAddress)
        hncol = cls.cols.index(H.HostName)
        if not cls.fmts:
            return rows
        M = [list(l) for l in rows]
        [all_stations.pop(r[pacol], 0) for r in M if r[pacol] in all_stations]
        for i, f in cls.fmts:
            for r in M:
                if r[pacol] in all_stations:
                    all_stations.pop(r[pacol], 0)
                r[i] = f(r[i], r, M)
        for pa, hn in all_stations.items():
            M.append(cls.inactive_station_row(pa, hn, pacol, hncol))
        return M

    @classmethod
    def inactive_station_row(cls, pa, hn, pacol, hncol):
        r = ['' for i in range(len(cls.cols))]
        r[pacol] = f'<span style="color:#999!important">{pa}</span>'
        r[hncol] = f'<span style="color:#999!important">{hn}</span>'
        return r

    @classmethod
    def no_entries(cls, data):
        data['table'] = div('', f'❌No results for {data["id"]}...')
        return data

    @classmethod
    def build(cls, id, data, ts=None, listen=None, all_stations=None, live=None):
        cpeid = data['id']
        ts_o = db.ts_hosts_oldest_cached(cpeid)
        if not ts_o:
            return cls.no_entries(data)

        if live:
            ts = time.time()
            reslt = live_hosts(cls.cols, live)
            templ = html.t_stations_table_data
        else:
            templ = html.t_stations_table
            if ts is None:
                ts = db.ts_stations_newest(cpeid)
            if not all_stations:
                all_stations = dict(db.all_stations(cpeid))
            reslt = db.stations(cpeid, cls.ch_cols, ts=ts)
        if not reslt:
            return cls.no_entries(data)
        rows = cls.apply_formatters(reslt, dict(all_stations))
        C = html.t_cell
        trows = trs([''.join([C % c for c in r]) for r in rows])
        # scroll = 'setTimeout(()=> window.scrollBy(0, 1000), 30)'
        head = thead(id_head(id), cls.head_row, listen=listen)  # , onclick=scroll)
        lt = live_toggle(id, listen) if id_live(id) in listen else ''
        data['table'] = render(
            templ,
            id=id + '-cht',
            title='Connected Stations',
            head=head,
            rows=trows,
            ts=ts,
            live_toggle=lt,
        )
        data['id'] = id + '-cht'
        data['all_stations'] = all_stations
        return data


def live_toggle(id, listen):
    return span(
        id_live(id),
        '',
        tooltip='Refresh',
        glyph='refresh',
        listen=listen,
    )


one_week = 7 * 86400


class station_charts:
    col_by_title = dict([[title(c), c] for c in stations_table.cols])
    t_kpi_chart = js_tmpl('../js/highcharts_kpi.js', True)

    @classmethod
    def build(cls, id, cpeid, col_titl, ts_from=None, listen=None):
        ts_from = ts_from or (time.time() - one_week)
        col = cls.col_by_title[col_titl]
        l = locals()
        l.pop('cls')
        if is_vcol(col):  # many charts
            return lsjoin([cls.select_chart_by_col(c, l) for c in col[1].cols])
        else:
            return cls.select_chart_by_col(col, l)

    @classmethod
    def select_chart_by_col(cls, col, l):
        l['col'] = col
        if issubclass(col, int):
            return cls.kpi_chart(**l)
        return ''

    @classmethod
    def kpi_chart(cls, col, id, cpeid, ts_from, **kw):
        idc = id + '-' + col.__name__
        result = db.stations_kpi(cpeid, ch_getter(col), ts_from)
        if not result:
            data = []
        else:
            R = {}

            def f(d, R=R):
                h, m, ts, v = d
                if v == 0:
                    return
                n = f'[{m[-3:]}] {h[:20]}'
                R.setdefault(n, []).append([ts, v])

            data = [f(d) for d in result]

            def tol(n, v):
                return {'name': n, 'data': v}

            data = [tol(n, v) for n, v in R.items()]

        c = render(
            cls.t_kpi_chart,
            id=idc,
            title=title(col),
            point_evts=point_events(idc, col, kw.get('listen')),
            y_title='Stations',
            data=data,
            ts_oldest=1000 * ts_from,
            ts_newest=1000 * int(time.time()),
        )
        return div(idc, script('', c))


def point_events(id, col, listen):
    """evt usually click - but app might specify more"""
    if not listen:
        return '{}'
    pl = listen.get('point')
    if not pl:
        return '{}'
    if not isinstance(pl[0], list):
        pl = [pl]
    js = []
    T = '%s: function() { if (axui.ctrl_key_down) axui.bus("%s", {x:this.category, y:this.y})}'
    for evt, cb in pl:
        topic = id + '-' + evt
        if topic not in HxEvts:
            HxEvts[topic] = cb
        js.append(T % (evt, topic))
    return '{%s}' % ','.join(js)


def round_time(dt, round_to):
    seconds = (dt - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)
