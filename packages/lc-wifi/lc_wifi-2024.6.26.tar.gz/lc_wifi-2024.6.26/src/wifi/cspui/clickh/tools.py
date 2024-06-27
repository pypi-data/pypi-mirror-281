from functools import lru_cache, cache, partial
from wifi.cspui.tools import span
from ax.utils.ax_tree import ax_tree
from wifi.vendors.vendors import vendors

"""
The actual complexity is, that sometimes MULTIPLE columns are displayed, with ONE title
=> there can be only one col click handler


We resolve then to displaying TWO charts, one per KPI shown.
That class here shall help a bit resolving the different handling.

"""

# ---------------------- Cols vs VCols ----------------------------------


def is_vcol(col):
    # is col a clickhouse table def col (a class) or a compound of many cols
    return isinstance(col, list)


def concat(cols, seperator=' '):
    sep_ = f", '{seperator}', "
    gs = [(title(c), ch_getter(c)) for c in cols]
    cols_ = cols

    class compound:
        cols = cols_  # required for the chart
        ch_getters = gs
        ch = 'concat(%s)' % sep_.join(['toString(%s)' % s[1] for s in gs])
        sep = seperator

    return compound


def ch_getter(c):
    return c[1].ch if is_vcol(c) else getattr(c, 'ch', c.__name__)


def ch_getters(cols):
    return ', '.join([ch_getter(c) for c in cols])


def title(c):
    return c[0] if is_vcol(c) else getattr(c, 'title', c.__name__)


def formatters(cols):
    l = []
    for i, c in zip(range(len(cols)), cols):
        if is_vcol(c) and len(c) > 2:
            l.append([i, c[2]])
            continue
        if hasattr(c, 'fmt'):
            l.append([i, c.fmt])
    return l


# ---------------------- DB ----------------------------------------------
def con():
    from operators.con.clickhouse import clickhouse  # TODO

    return clickhouse


@cache
def ts_stations_oldest(cpeid):
    return ts_stations(cpeid, desc='')


def ts_stations(cpeid, desc):
    ch = con()
    ts_q = f"SELECT toUnixTimestamp(ts) FROM hosts WHERE id = '{cpeid}' ORDER BY ts {desc} LIMIT 1"
    ts_q_r = ch.get(ts_q)
    if ts_q_r:
        return ts_q_r.result_rows[0][0]


class db:
    ts_hosts_oldest_cached = ts_stations_oldest

    def ts_stations_newest(cpeid):
        return ts_stations(cpeid, desc='DESC')

    def all_stations(cpeid, ts_from=None):
        ts = ts_from or ts_stations_oldest(cpeid)
        query = f"SELECT DISTINCT PhysAddress, HostName FROM hosts WHERE id = '{cpeid}' AND toUnixTimestamp(ts) > {ts}"
        result = con().get(query)
        if result:
            return result.result_rows

    def stations(cpeid, cols, ts):
        query = f"SELECT {cols} FROM hosts WHERE id = '{cpeid}' AND toUnixTimestamp(ts) == {ts}"
        result = con().get(query)
        if result:
            return result.result_rows

    def stations_kpi(cpeid, col, ts_from):
        query = f"SELECT HostName, PhysAddress, toUnixTimestamp(ts) * 1000, {col} FROM hosts WHERE id = '{cpeid}' AND toUnixTimestamp(ts) >= {ts_from} ORDER BY ts ASC"
        result = con().get(query)
        if result:
            return result.result_rows

    def all_radio_kpi(cpeid, cols, ts_from):
        query = f"SELECT toUnixTimestamp(ts) * 1000, {cols} FROM timeseries WHERE id = '{cpeid}' AND toUnixTimestamp(ts) >= {ts_from} ORDER BY ts ASC"
        result = con().get(query)
        if result:
            return result.result_rows


def active(m, t={'1', 1, 'true', True}):
    return m.get('Active') in t


def host_name(host):
    n = host['HostName']
    if len(n) > 20:
        n = n[:20] + '..'
    return n


def live_val(host, col, all):
    n = col.__name__
    if n == 'vendor':
        mac = host.get('PhysAddress', '')
        return vendors.get(mac.replace(':', '')[:6], '---')
    if n == 'PhysAddress':
        return host.get('PhysAddress', '')
    if n == 'IPAddress':
        return host.get('IPAddress', '')
    if n == 'InterfaceType':
        return host.get('InterfaceType', '')
    if n == 'standard':
        return all['iface'].get('MediaType', '').replace('IEEE 802.', '')
    if n == 'SignalStrength':
        v = -int(all['metric']['RSSI'])
        if v == -255:
            v = 0
        return v
    if n == 'LastDataDownlinkRate':
        return int(all['metric']['X_AVM-DE_PHYRateRX'])
    if n == 'LastDataUplinkRate':
        return int(all['metric']['X_AVM-DE_PHYRateTX'])
    if n == 'band':
        f = int(all['iface']['X_AVM-DE_PrimaryFrequency'])
        return '5' if f > 5000000 else '2' if f > 2000000 else ''
    if n == 'ssid':
        return ''
    if n == 'snr':
        return 0
    if n == 'ErrorsReceived':
        return 0
    if n == 'ErrorsSent':
        return 0
    if n == 'BytesReceived':
        return 0
    if n == 'BytesSent':
        return 0
    if n == 'PacketsReceived':
        return 0
    if n == 'PacketsSent':
        return 0
    if n == 'Retransmissions':
        return 0
    if n == 'RetransCount':
        return 0

    if issubclass(col, int):
        return 0
    return col.__name__


def live_vals(n, host, cols, all):
    r = ()
    try:
        i = host['AssociatedDevice']

        all[1905] = i = all['data'][i]
        all['iface'] = i['Interface']['1']
        try:
            all['metric'] = i['IEEE1905Neighbor']['1']['Metric']['1']
        except Exception as ex:
            # went inactive, hosts may still show active for a while
            return

        for c in cols:
            if is_vcol(c):
                c = c[1]
                r += ((c.sep).join([str(live_val(host, i, all)) for i in c.cols]),)
            elif c.__name__ == 'HostName':
                r += (n,)
            else:
                r += (live_val(host, c, all),)
    except Exception as ex:
        app.error('live vals', ex=ex)
        return None

    return r


from devapp.app import app


def live_hosts(cols, data):
    data = ax_tree.AXTree(data)
    T = data['Device.IEEE1905']['AL']['NetworkTopology']
    hosts = {}
    ieee = T['IEEE1905Device']
    all = {'hosts': hosts, 'mesh': {'master': None}, 'ieee': ieee, 'data': data}
    Hosts = data['Device.Hosts.Host']
    for k, host in Hosts.items():
        if not active(host):
            continue
        n = host_name(host)
        lv = live_vals(n, host, cols, all)
        if lv:
            hosts[n] = lv
    ret = [hosts[n] for n in sorted(hosts)]
    return ret


# ---------------------- UI ----------------------------------------------


@cache
def link_symbol(s):
    ico = ''
    n = s.split(' ', 1)[-1]  # e.g. 11ac
    if 'WiFi' in s:
        b = n
        t = 'IEEE 802.' + s
        ico = 'signal'
        cc = {'11ac': 'black', '11n': 'black', '11g': 'black'}
        c = cc.get(s, cc['11g'])
    elif 'Ether' in s:
        b, t, c = f'<b>🖧 </b>&nbsp;&nbsp; GbE', 'IEEE 802.3ab (Gigabit Ethernet)', 'black'
        if '3u' in s:
            b, t, c = f'<b>🖧 </b>&nbsp;&nbsp; FE', 'IEEE 802.3u (Fast Ethernet)', 'black'
    else:
        b, t, c = '', 'Other Link (Not reported by CPE)', '#ccc'
        ico = 'link'
    kw = {'glyph': ico} if ico else {}
    return span('', b, tooltip=t, style=f'color:{c};min-width:7rem', **kw)


class fmt:
    def link(s, row, table):
        # the other cols are available at actual formatting time. we *could* display a .) signal for bad wifi
        return link_symbol(s)
