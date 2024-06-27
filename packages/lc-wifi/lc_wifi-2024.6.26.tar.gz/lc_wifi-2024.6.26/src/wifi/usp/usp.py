"""
USP Specific Functions
"""
import time
from ax.utils.ax_tree import AXTree
import requests
import json
from devapp.tools import get_deep, cast as simple_cast
from devapp.app import app
from absl import flags
from operators.con import add_connection, redis, con
from wifi.api import job_timeout, api_activity_key, api2
from time import sleep


flags.DEFINE_string(
    'axusp_api_endpoint',
    default='http://{c_nbi}',
    help='RPC API endpoint to AXUSP controller, or format string to translate reported c_nbi to reachable endpoints',
)

flags.DEFINE_integer(
    'usp_c_nbi_expiry',
    default=3600 * 24 * 30,
    help='How long to keep c_nbi entries in Redis',
)

flags.DEFINE_integer(
    'usp_c_nbi_http_keepalive',
    default=300,
    help='How long to keep c_nbi HTTP connections open',
)

flags.DEFINE_integer(
    'usp_c_nbi_http_keepalive_pools',
    default=32,
    help='How many connection pools to maintain, should be equal to or larger than number of controllers',
)

# https://usp.technology/specification/index.htm#sec:use-of-authority-scheme-and-authority-id
usp_schemes = {
    'oui',
    'cid',
    'pen',
    'self',
    'user',
    'os',
    'ops',
    'uuid',
    'imei',
    'proto',
    'doc',
    'fqdn',
}

BULBS = {'promoted': '🟩', 'connect': '🟨', 'disconnect': '🟥'}


def is_usp_id(epid, _pref=usp_schemes):
    # FIXME: fix within flows ("Is USP" pycond) - use this function
    if epid.split(':', 1)[0] in _pref:
        return True


# leave this value str type when casting protobuf:
cast_leave = {'802.11'}


def cast(v, leave=cast_leave, c=simple_cast):
    """protobuf just delivers strings"""
    if v in cast_leave:
        return v
    try:
        return c(v)
    except Exception:
        return v


def cast_deep(m, cast=cast):
    r = AXTree({})
    for k, v in AXTree(m).iter_leaf_items():
        r[k] = cast(v)
    return r


def patched_update_redis(data, msg=None):
    msg = msg or {}
    p = data.get('body') or data
    p['ts'] = data.get('ts', time.time())
    id = p['id']
    if 'type' in data:
        p['job_expiry'] = data.get('ttl', job_timeout(data['type']))
        # data['type'] = data['type'].capitalize()
    try:
        m = p['result']['msg']
        m = m[0].upper() + m[1:]
        c = p['result']['code']
        if c > 299:
            m = f'❗{m}'
        p['result']['msg'] = m

    except Exception:
        pass
    if p.get('path') == '/progress':
        p['job_expiry'] = 0
    if p.get('path') == '/written':
        p['update_ui'] = True
        p['result']['msg'] = '💾 KPIs stored'
    elif p.get('path') == '/finish':
        if 'result' not in p:
            p['result'] = {'msg': 'forced finish', 'code': 200}
        if not is_usp_id(id):
            p['update_ui'] = True

    con.redis.set_events({'evt': p}, msg=msg, key=f'apijob:{id}')

    if p.get('path') == '/finish':
        time.sleep(0.001)
        api_start(id, '', '♾ Keep listening...', ttl=0)

    if p.get('path') == '/written':
        if is_usp_id(id):
            time.sleep(0.002)
            p['path'] = '/finish'
            p['result']['msg'] = '..'
            con.redis.set_events({'evt': p}, msg=msg, key=f'apijob:{id}')


def api_log_when_active(id, typ, data):
    if not con.redis.get({}, {}, key=api_activity_key(id)):
        return

    if typ == 'axwifi_realtime_valuechange':
        k, v = list(data['data'].items())[0]
        txt = f'{k[7:]}: {v}'
    else:
        txt = f'{typ} ({len(str(data))}B)'

    api_upd(id, f'⎆ {txt}')


def api_start(id, msg, type, ttl=100):
    return api2.update_redis({'type': type, 'ttl': 0, 'id': id})


def api_fin(id, msg, code=200):
    return api_upd(id, msg, code, path='/finish')


def api_upd(id, msg, code=200, path='/progress'):
    d = {
        'id': id,
        'path': path,
        'result': {
            'code': code,
            'msg': msg,
        },
    }
    api2.update_redis(d)


add_connection(redis.redis, 'axredis')


LightScanParams = [
    [
        'Device.BulkData.Profile.1.ReportingInterval',
        'Device.DeviceInfo.ProcessStatus.CPUUsage',
        'Device.DeviceInfo.ProductClass',
        'Device.DeviceInfo.SerialNumber',
        'Device.DeviceInfo.SoftwareVersion',
        'Device.DeviceInfo.UpTime',
        'Device.Hosts.Host.',
        'Device.WiFi.AccessPoint.',
        'Device.WiFi.Radio.',
        'Device.WiFi.SSID.',
        'Device.LocalAgent.Controller.',
        # 'Device.LocalAgent.Controller.1.MTP.*.Enable',
        # 'Device.LocalAgent.Controller.1.MTP.*.Protocol',
        'Device.DeviceInfo.HardwareVersion',
        'Device.DeviceInfo.Manufacturer',
        'Device.DeviceInfo.ManufacturerOUI',
        'Device.DeviceInfo.MemoryStatus.Free',
        'Device.DeviceInfo.MemoryStatus.Total',
        'Device.DeviceInfo.ModelName',
        'Device.Ethernet.Link.',
        'Device.IEEE1905.AL.NetworkTopology.',
    ],
    0,
]


def dt(t0):
    return int(1000 * (time.time() - t0))


class axiros_controller:
    """This is currently only one: The Axiros Controller"""

    HDR = {
        'Connection': 'Keep-Alive',
        'Keep-Alive': 'timeout=',
        'Content-Type': 'application/json'
    }
    conn_pool = None

    @classmethod
    def rpc(contr, jobd, data):
        if contr.conn_pool is None:
            contr.conn_pool = requests.Session()
            contr.HDR['Keep-Alive'] += str(flags.FLAGS.usp_c_nbi_http_keepalive)
            contr.conn_pool.headers.update(contr.HDR)
            contr.conn_pool.mount('http://', requests.adapters.HTTPAdapter(
                pool_connections=flags.FLAGS.usp_c_nbi_http_keepalive_pools,
                pool_maxsize=4,    # number of connections per pool, possibly not necessary
                pool_block = True  # wait until a connection is available
            ))

        patch = getattr(contr.vendor_patches, jobd['typ'], None)
        if patch:
            patch(jobd, data)

        return contr.conn_pool.post(
            jobd['c_nbi'] + jobd['path'],
            json.dumps(jobd['body']),
            timeout=jobd['timeout']
        )


def is_avm(jobd, data):
    di = data.get('props')
    if di:
        return di['Device.DeviceInfo.Manufacturer']


class usp:
    """The usp function tree for NodeRed"""

    c_nbi_by_epid = {}  # local cache to avoid unnecessary load on Redis
    last_c_nbi_rst_by_epid = {}

    class controller(axiros_controller):
        class vendor_patches:
            def operate(jobd, data):
                if jobd['body']['command'] == 'Device.WiFi.NeighboringWiFiDiagnostic()':
                    if is_avm(jobd, data):
                        jobd['body']['args'] = [['X_AVM-DE_ForceRescan', 'true']]

    @classmethod
    def c_nbi_redis_key(usp, epid):
        return f'usp_c_nbi::{epid}'

    @classmethod
    def remove_local_c_nbi(usp, epid):
        usp.last_c_nbi_rst_by_epid.pop(epid, None)
        return bool(usp.c_nbi_by_epid.pop(epid, False))

    @classmethod
    def reset_c_nbi_expiry(usp, epid):
        last_rst = usp.last_c_nbi_rst_by_epid.get(epid, 0)
        cur_time = time.time()

        if cur_time - last_rst <= 10:
            # reset at most every 10 seconds
            return

        usp.last_c_nbi_rst_by_epid[epid] = cur_time
        con.redis.expire({}, {}, usp.c_nbi_redis_key(epid), flags.FLAGS.usp_c_nbi_expiry)
        app.debug('Reset c_nbi expiry in Redis.', cpe=epid)

    @classmethod
    def save_c_nbi(usp, data):
        epid = data.get('id', data.get('epid'))
        if not epid:
            app.error('No epid in connect notification.', data=data)
            return

        try:
            c_nbi = data['data']['c_nbi']
        except KeyError:
            app.error('No c_nbi in connect notification.', data=data)
            return

        usp.c_nbi_by_epid[epid] = c_nbi

        con.redis.set(
            c_nbi,
            {},
            usp.c_nbi_redis_key(epid),
            ex=flags.FLAGS.usp_c_nbi_expiry,
            enc='plain',
        )

        app.debug(
            'Saved c_nbi locally and to Redis.',
            cpe=epid,
            c_nbi=c_nbi,
        )
        return data

    @classmethod
    def get_c_nbi(usp, epid, force_redis=False):
        c_nbi = usp.c_nbi_by_epid.get(epid)
        if not c_nbi or force_redis:
            c_nbi = con.redis.get({}, {}, usp.c_nbi_redis_key(epid), enc='plain')
            if c_nbi:
                usp.c_nbi_by_epid[epid] = c_nbi
                app.debug('Got c_nbi from Redis.', cpe=epid, c_nbi=c_nbi)
            else:
                usp.remove_local_c_nbi(epid)
                app.warning(
                    'No c_nbi stored in Redis for USP CPE, probably offline.', cpe=epid
                )
                return ''

        return flags.FLAGS.axusp_api_endpoint.format(
            c_nbi=c_nbi
        )  # todo: define a dict or function somewhere to use here

    @classmethod
    def remove_c_nbi(usp, data):
        epid = data.get('id', data.get('epid'))
        if not epid:
            app.error('No epid in disconnect notification.', data=data)
            return

        try:
            disconnected_c_nbi = data['data']['c_nbi']
        except KeyError:
            app.error(
                'No c_nbi in disconnect notification, please update USP controller.',
                data=data,
            )
            return

        # remove only if the disconnect corresponds to stored c_nbi
        # because disconnects due to timeout may come in after a connect
        # whose connection is still valid
        if usp.c_nbi_by_epid.get(epid) == disconnected_c_nbi:
            if usp.remove_local_c_nbi(epid):
                app.debug('Removed c_nbi locally.', cpe=epid)

        r = {}
        con.redis.compare_unset({}, r, usp.c_nbi_redis_key(epid), disconnected_c_nbi)
        if next(iter(r.values())):
            app.debug('Removed c_nbi from Redis.', cpe=epid)

        return data

    @classmethod
    def job(usp, data, msg=None, err_info=True):
        id = data.get('id') or data['epid']
        usp_job = data.get('usp_job', data)  # old format
        typ = usp_job['type']
        body = usp_job['body']
        t0 = time.time()
        jobd = {
            'timeout': usp_job.get('timeout', 5),
            'c_nbi': usp.get_c_nbi(id),
            'path': f'/v1/{id}/{typ}',
            'typ': typ,
            'body': body,
        }
        try:
            # if typ == 'operate': breakpoint()  # FIXME BREAKPOINT
            res = usp.controller.rpc(jobd, data)
            if res.status_code == 404:
                # local cache could have wrong c_nbi for the CPE
                # query redis and try again
                redis_c_nbi = usp.get_c_nbi(id, force_redis=True)
                if redis_c_nbi != jobd['c_nbi']:
                    app.debug(
                        'USP controller returned 404, retrying with correct c_nbi from Redis.',
                        cpe=id,
                    )
                    jobd['c_nbi'] = redis_c_nbi
                    res = usp.controller.rpc(jobd, data)
            s = res.status_code
            if 200 <= s <= 299:
                # success
                usp.reset_c_nbi_expiry(id)
            r = res.text
            l = len(r)  # noqa: E741
            txt = f'Status {s} {dt(t0)}ms {l}B'
            try:
                r = json.loads(r)
            except Exception:
                pass
        except Exception as ex:
            r = txt = str(ex)
            s = 500
        sleep(0.001)  # redis / UI
        if typ == 'operate':
            typ = f'{typ} {body["command"]}'
        txt = f'⚙️ /{typ.ljust(10)}: {txt}'
        api_upd(id, txt, s)

        data['resp_status'] = s
        data['resp'] = r
        try:
            res = r['Response']['GetResp']['req_path_results']
            m = {}

            def add(m, pth, params):
                n = {pth + k: params[k] for k in params}
                m.update(n)

            def jobd(k, m):
                for i in k['resolved_path_results']:
                    add(m, i['resolved_path'], i['result_params'])

            [jobd(k, m=m) for k in res]
            data['resp_dict'] = m
        except Exception:
            pass

    @classmethod
    def enforce(usp, data):
        id = data['id']
        j = None
        for d in data, data['collector']:
            try:
                j = d['job']['steps']['1']['MappedSetParameterValues']
                break
            except Exception:
                pass
        if not j:
            api_fin(id, 'No changes to be enforced')
            return {'a': 'b'}

        r = {}

        def add(node, leaf, v):
            h = r.setdefault(node + '.', [])
            h.append([leaf, str(v), True])

        j = {k: v for k, v in AXTree(j).iter_leaf_items()}
        m = {}
        new = {}
        for k, v in j.items():
            node, leaf = k.rsplit('.', 1)
            N = data.get(node)
            o = N.get('orig_' + leaf)
            if o:
                l = o.split(':')
                leaf = leafui = l.pop(0)
                for val_proc in l:
                    if val_proc == 'int':
                        v = int(v)

            leafui = leaf
            o = N.get('orig_node')
            if o:
                leafui = f'..{leaf}'
                node = o
            else:
                o = N.get('idx_orig')
                new[k] = v
                if o:
                    leafui = f'..{o}.{leaf}'
                    node = node.rsplit('.', 1)[0] + f'.{o}'
            m[leafui] = v
            v = str(v).replace('False', 'false').replace('True', 'true')
            add(node, leaf, v)

        if r:
            r = [[k, v] for k, v in r.items()]
            job = {
                'timeout': 20,  # jointelli...
                'type': 'set',
                'epid': id,
                'body': {
                    'allow_partial': True,
                    'update_objs': r,
                },
            }
            app.info('set job', json=r)
            usp.job(job, err_info=False)
            m = ' '.join([f'{k}:{v}' for k, v in m.items()])
            if 'oper_failure' in str(job):
                code = 400
                m = 'Failed ' + m
            else:
                code = 200
                m = f'✔️ {m}'
                data.update(new)
            api_fin(id, m, code=code)

    @classmethod
    def has_cwmp_style_fullscan_subscr(usp, data):
        job = {
            'type': 'get',
            'epid': data.get('id', data.get('epid')),
            'body': [
                [
                    'Device.LocalAgent.Subscription.[ID=="axwifi_realtime_wifidiagnostics"].'
                ],
                1,
            ],
        }
        data['usp_job'] = job
        usp.job(job, msg='Checking for CWMP-style NeighboringWiFiDiagnostic subscription')
        app.debug(
            'CWMP-style NeighboringWiFiDiagnostic subscription check result', job=job
        )
        subscriptions = job.get('resp_dict')
        if subscriptions is None:
            return False
        return bool(len(subscriptions))

    @classmethod
    def req_cwmp_style_fullscan(usp, data):
        job = {
            'type': 'set',
            'epid': data.get('id', data.get('epid')),
            'body': {
                'allow_partial': False,
                'update_objs': [
                    [
                        'Device.WiFi.NeighboringWiFiDiagnostic',
                        [['DiagnosticsState', 'Requested', True]],
                    ]
                ],
            },
        }
        data['usp_job'] = job
        usp.job(job, msg='Requesting CWMP-style NeighboringWiFiDiagnostic')
        app.debug('CWMP-style NeighboringWiFiDiagnostic request result', job=job)

    @classmethod
    def fetch_cwmp_style_fullscan_results(usp, data):
        job = {
            'type': 'get',
            'epid': data.get('id', data.get('epid')),
            'body': [['Device.WiFi.NeighboringWiFiDiagnostic.Result.'], 0],
        }
        usp.job(job, msg='Fetching CWMP-style NeighboringWiFiDiagnostic result')
        data['cwmp_style_fullscan_result'] = job.get('resp_dict')

    @classmethod
    def format_cwmp_style_fullscan(usp, data):
        results_orig = data.get('cwmp_style_fullscan_result')
        if results_orig is None:
            return

        results = {'Status': 'Success'}
        for param, value in results_orig.items():
            param = param.replace('Device.WiFi.NeighboringWiFiDiagnostic.', '', 1)
            results[param] = value

        data.update({'type': 'fullscan', 'data': results})

    @classmethod
    def req_fullscan(usp, data, msg=None):
        if usp.has_cwmp_style_fullscan_subscr(data):
            app.debug(
                'CPE has CWMP-style fullscan complete subscription. '
                'Requesting CWMP-style fullscan.'
            )
            return usp.req_cwmp_style_fullscan(data)
        else:
            app.debug('Requesting USP standard-compliant fullscan.')
            return usp.req_operate(data, type='fullscan')

    class lightscan:
        # @classmethod
        # def get_res_to_bulk_fmt(ls, data):
        #     d = data['resp_dict']
        #     d['CollectionTime'] = int(time.time())
        #     epid = data['epid']
        #     cepid = 'proto::controller'
        #     r = to_bulk_fmt(cepid, epid, d)
        #     return r

        @classmethod
        def to_tr181(ls, data):
            """patched when we have non std ones"""
            return

        @classmethod
        def params_by_cpeid(ls, _):
            """patched when we have non std ones"""
            return LightScanParams

        @classmethod
        def get(ls, data):
            id = data['id']
            params = ls.params_by_cpeid(id)
            job = {'type': 'get', 'epid': id, 'body': params, 'timeout': 20}
            usp.job(job)
            r = job.get('resp_dict')
            if not r:
                api_fin(id, 'RPC failed with controller', code=400)
                raise Exception(f'RPC failed {r}')
            api_upd(id, 'Got WiFi state.')
            if 'interval' in data:
                r['Device.BulkData.Profile.1.ReportingInterval'] = data['interval']
            data['props'] = r

        @classmethod
        def to_redis(ls, data):
            id = data['id']
            key = f'light_scan::{id}'
            con.redis.set(data, {}, key, ex=200)  # FIXME
            return data

        @classmethod
        def from_redis(ls, data):
            id = data['id']
            key = f'light_scan::{id}'
            r = con.redis.get({}, {}, key)
            if not r:
                return app.warn('No lightscan data')
            data['lightscan'] = con.redis.get({}, {}, key)

    @classmethod
    def req_operate(usp, data, msg=None, type=None):
        id = data['id']
        # backward compat, then no vendor hooks will work
        type = type or data.get('type')
        if type == 'reboot':
            cmd = 'Device.Reboot()'
        elif type == 'factory_reset':
            cmd = 'Device.FactoryReset()'
        elif type in {'refresh', 'optimize', 'fullscan'}:
            cmd = 'Device.WiFi.NeighboringWiFiDiagnostic()'
        else:
            raise Exception('unsupported cmd')
        job = {
            'type': 'operate',
            'epid': id,
            'body': {
                'command': cmd,
                'command_key': f'{type}',
                'send_resp': True,
                'args': [],
            },
        }
        data['usp_job'] = job
        usp.job(data)

    class msg_fmt:
        def axwifi_realtime_valuechange(data, details):
            """
            "data": {
                  "param_path": "Device.Hosts.Host.1.WANStats.PacketsSent",
                  "param_value": "77955"
              },
              "epid": "epid",
              "type": "axwifi_realtime_valuechange"
            """
            d = details['value_change']
            k, v = d['param_path'], cast(str(d['param_value']))
            return {k: v}

        def fullscan(data, details):
            d = details['oper_complete']
            try:
                d = d.get('req_output_args')['output_args']
            except Exception:
                d = {'Status': 'Error', 'err': d.get('cmd_failure')}
            return d

        def lightscan(data, details):
            d = details['event']['params']['Data']
            return json.loads(d) if isinstance(d, str) else d

        unknown = 'unknown'
        val_change = 'val_change'

    @classmethod
    def qualify_msg(usp, data: dict, msg: dict):
        """All leave with 'type', 'id', 'data'"""
        epid = 'unknown_epid'
        try:
            if not 'c_epid' in data:
                # redis src places the payload deeper
                # todo: possibly distinguish by source type
                data = data['data']['payload']
            epid = data.get('epid', '')
            if 'details' not in data:  # general notifications
                typ = data.get('type', 'skip')
                data = {'data': data, 'type': typ}
                if typ in ('connect', 'promoted', 'disconnect') and epid:
                    # cpe status notification
                    status = BULBS[typ]
                    api_upd(epid, f'{status} CPE {typ}')
                elif typ == 'shutdown':
                    # controller shutdown
                    pass
                else:
                    data['type'] = 'skip'
                    app.info('discarding', payload=data)
            else:  # subscription messages
                det = data['details']
                typ = det['subscription_id']
                if typ == 'axwifi_realtime_operationcomplete':
                    cmd_key = det['oper_complete']['command_key']
                    if cmd_key in {'refresh', 'optimize', 'fullscan'}:
                        typ = 'fullscan'
                elif typ == 'axwifi_realtime_wifidiagnostics':
                    changed = det.get('value_change', {})
                    param = changed.get('param_path')
                    val = changed.get('param_value')
                    if param.endswith('.DiagnosticsState') and val == 'Complete':
                        typ = 'cwmp_style_fullscan'
                elif typ == 'axwifi_push':
                    typ = 'lightscan'
                elif typ == 'axwifi_realtime_events':
                    event = det['event']
                    prms = event.get('params', {})
                    event_name = event.get('event_name', {})
                    cause = prms.get('Cause', '').lower()
                    if 'Boot!' in event_name:
                        typ = 'factory_reset' if 'factory' in cause else 'boot'
                    # no job over reboots
                    api_fin(epid, '🔛 CPE up again')

                fmt = getattr(usp.msg_fmt, typ, '')
                if fmt:
                    data = {'data': fmt(data, det)}
                else:
                    data = {'data': det}
                api_log_when_active(epid, typ, data)
                data['type'] = typ
        except Exception as prms:
            raise
        data['id'] = data['z'] = epid  # e.g. for log
        data['log'] = []
        app.info(data['type'], cpe=epid)
        return data

    @classmethod
    def to_datamodel(usp, data, msg):
        """we have either lightscan only, ls with fs or fs"""
        job = None
        fullsc = None
        cast_ = False
        props = None

        if data['type'] == 'reconfigure':
            cast_ = True
            props = data['props']
            job = data.pop('job')
            job['type'] = 'reconfigure'

        elif data['type'] in {'refresh', 'lightscan.get'}:
            # light = true
            props = data['props']
            cast_ = True

        elif data['type'] == 'lightscan':
            props = data.pop('data')['Report'][0]

        elif data['type'] == 'fullscan':
            fullsc = data.pop('data')
            ls = data.pop('lightscan')
            rep = ls.get('data', {}).get('Report')
            if rep:
                props = rep[0]
            else:
                props = ls.pop('props')
                cast_ = True
                # from redis:
                job = ls

        if not props:
            breakpoint()  # FIXME BREAKPOINT
        if cast_:
            props = {
                k: cast(v) for k, v in props.items() if not k.endswith('InterfaceType')
            }
        usp.normalize_lightscan_from_bulk(props, into=data)
        if job:
            data['props']['collector']['job'] = job
        r = {
            'ts': int(time.time() * 1000),
            'cpeid': data['id'],
            'sender': {
                'name': 'axusp_collector',
            },
        }
        data.update(r)
        if not fullsc:
            return data
        if fullsc['Status'] in ['Complete', 'Success']:
            usp.normalize_fullscan(fullsc, into=data)
            dt = int(1000 * (time.time() - msg['ts']))
            data['props']['WiFi']['NeighboringWiFiDiagnostic']['scan_dt'] = dt
            data['type'] = 'fullscan_norm'
            fsm = {'light_scan': 0, 'full_scan': 1, 'msg': 'Full Scan'}
            data['props']['collector'].update(fsm)
        else:
            try:
                txt = fullsc['err']['err_msg']
                txt = f'CPE reports: "{txt}"'
            except Exception:
                txt = 'Missing scan data'
            api_upd(data['id'], txt, 305)

    def fix_radio_params(props):
        subtree = 'WiFi.Radio'

        # <abstract_param>: (normalize_func, (<dev_params>))
        mapping = {
            'Enable': (lambda v: bool(int(v)), ('Enabled', 'Channel', 'Status')),
        }

        radios = props.get(subtree)
        if not radios:
            return

        for i in radios:
            radio = radios[i]

            for abstract_param, (normalize_func, dev_params) in mapping.items():
                abstract_param_full = f'{subtree}.{i}.{abstract_param}'

                # parameter might already exist in radio
                value = radio.get(abstract_param)

                if value is None:
                    # parameter doesn't exist, look for value using dev_params
                    for dev_param in dev_params:
                        if '.' in dev_param:
                            value = props.get(dev_param)
                        else:
                            value = radio.get(dev_param)
                        if value is not None:
                            break

                if value is None:
                    app.warning(
                        'usp.fix_radio_params(): unable to get parameter',
                        radio=radio,
                        param=dest_param_full,
                    )
                    continue

                try:
                    value = normalize_func(value)
                except Exception as e:
                    app.warning(
                        'usp.fix_radio_params(): unable to normalize parameter value',
                        radio=radio,
                        param=dest_param_full,
                        value=value,
                        ex=str(e),
                    )
                    continue

                props[abstract_param_full] = value

    def normalize_lightscan_from_bulk(props, into):
        into['ts'] = props.pop('CollectionTime', time.time())
        props = AXTree(props)
        into['props'] = p = props.pop('Device')
        usp.fix_radio_params(p)
        p['collector'] = {
            'msg': 'Light Scan',
            'full_scan': 0,
            'code': 200,
            'details': '',
            'light_scan': 1,
        }
        into['type'] = 'lightscan_norm'

    def normalize_fullscan(data, into):
        d = AXTree(data)
        into['props']['WiFi']['NeighboringWiFiDiagnostic'] = d
        d['DiagnosticsState'] = d['Status']
        d['ResultNumberOfEntries'] = len(d['Result'])

    def normalize_tr181_indexes(data):
        """AXW Convention: All indizes (and refs) are 1-4 for 2 Ghz stuff
        and 5- ... for 5Ghz
        """
        t0 = time.time()
        props = data['props'].get('WiFi')
        if not props:
            return
        # e.g. replrad = {'Device.WiFi.Radio.2': 'Device.WiFi.Radio.5'}
        changed_radio_idxs = rearrange_idx_for_2_and_5(props, 'Radio', is2=radio_is_2ghz)
        for k in [
            ['SSID', 'LowerLayers'],
            ['NeighboringWiFiDiagnostic.Result', 'Radio'],
        ]:
            replace_refs_and_create_virtual_objs(props, k, changed_radio_idxs)

        changed_ssid_idxs = rearrange_idx_for_2_and_5(props, 'SSID', is2=low_lay_is_2ghz)
        replace_refs_and_create_virtual_objs(
            props, ['AccessPoint', 'SSIDReference'], changed_ssid_idxs
        )
        changed_api_idxs = rearrange_idx_for_2_and_5(
            props, 'AccessPoint', is2=ssid_ref_is_2ghz
        )
        app.info(
            'Normalized',
            dt=time.time() - t0,
            json={
                'radios': changed_radio_idxs,
                'ssids': changed_ssid_idxs,
                'aps': changed_api_idxs,
            },
        )

    def fake_hosts_active(data):
        # when no devicde is connected....
        h = data['props'].get('Hosts', {}).get('Host', {})
        for k, v in h.items():
            v['Active'] = True
            if k == '1':
                v['Active'] = 1


def radio_is_2ghz(r):
    return '5' not in r['OperatingFrequencyBand']


def ref_is_2ghz(r, ref):
    # rearranged lower layers already:
    return int(r[ref].rsplit('.', 1)[-1]) < 5


def low_lay_is_2ghz(r):
    return ref_is_2ghz(r, 'LowerLayers')


def ssid_ref_is_2ghz(r):
    return ref_is_2ghz(r, 'SSIDReference')


def replace_refs_and_create_virtual_objs(props, key, repl):
    if not repl:
        return
    o = get_deep(key[0], props, dflt=0)
    if not o:
        return

    # o has v e.g. like {'BSSID': '62:ED:6F:76:FD:97', 'LowerLayers': 'Device.WiFi.Radio.1,Device.WiFi.Radio.2'}
    # -> we find those multis and return them in a 'new' dict of artificial objects, with just a single ref
    new = {}
    do_single_repl_ref(o, key[1], repl, new=new)
    if new:
        do_single_repl_ref(new, key[1], repl, new)
        o.update(new)


def do_single_repl_ref(o, key, repl, new):
    for k in o:
        v = o[k]
        if key not in v.keys():
            continue
        old = v[key]
        if ',' not in old:
            n = repl.get(old, old)
            if not isinstance(n, list):
                v[key] = n
                continue
            multi = n
            v[key] = n[0]
        else:
            multi = [i.strip() for i in old.split(',')]
            v[key] = repl.get(multi[0], multi[0])
        for r in multi[1:]:
            nd = dict(v)
            nd['idx_virt'] = k
            nd[key] = repl.get(r, r)
            # find idx to insert the new artificial obj
            idx = len(o) + len(new) + 1  # idx start at 1
            while str(idx) in o or str(idx) in new:
                idx += 1
            new[str(idx)] = nd


def rearrange_idx_for_2_and_5(props, pth, is2, i2=0, i5=4):
    """Our convention was: all 2Ghz idxs are 1,2,.. and 5Ghzs ones 5,6...
    Do this here, but keep the original idx for later jobs:
    """
    repl = {}
    r = {}

    obj = props.get(pth)
    if not obj:
        return r
    for k, v in sorted(obj.items()):
        idx_orig = v.get('idx_virt', k)
        ref = f'Device.WiFi.{pth}.{idx_orig}'
        if is2(v):
            i2 += 1
            i = i2
        else:
            i5 += 1
            i = i5
        nref = f'Device.WiFi.{pth}.{i}'
        r[str(i)] = v
        v['idx_orig'] = idx_orig
        if nref != ref:
            v = repl.get(ref)
            if v:
                repl[ref] = v if isinstance(v, list) else [v]
                repl[ref].append(nref)
            else:
                repl[ref] = nref
    props[pth] = r
    return repl


# c = Functions.usp
# add_pre_post_hook(c, 'to_datamodel', fix_avm_lower_layers_end_dot)
#
# def add_pre_post_hook(cls, orig_func_name, hook, mode='pre'):
#     orig = getattr(cls, orig_func_name)
#     if mode == 'pre':
#
#         def h(data, msg=None, **kw):
#             data = hook(data, msg, **kw) or
#             return orig(hook(*a, **kw))
#
#     else:
#
#         def h(*a, **kw):
#             return hook(orig(*a, **kw))
#
#     setattr(cls, orig_func_name, h)

orig = usp.to_datamodel


def fix_avm_lower_layers_end_dot(data, msg=None, orig=orig):
    # some lower layer refs hava a dot at the end (only AVM)
    try:
        if 'props' in data:
            collection = data['props']
        elif 'lightscan' in data:
            ls = data['lightscan']
            if 'props' in ls:
                collection = ls['props']
            else:
                collection = ls['data']['Report'][0]
    except Exception:
        return orig(data, msg)

    def fix(v):
        if not v:
            return v
        # avm guest nw: 'Device.WiFi.SSID.3.LowerLayers': 'Device.WiFi.Radio.1.,Device.WiFi.Radio.2'}
        if ',' in v:
            return ','.join([fix(i.strip()) for i in v.split(',')])
        if not v.startswith('Device.'):  # zyxel
            v = 'Device.' + v
        return v[:-1] if v[-1] == '.' else v

    lls = {k: fix(collection[k]) for k in collection if k.endswith('.LowerLayers')}
    collection.update(lls)
    return orig(data, msg)


usp.to_datamodel = fix_avm_lower_layers_end_dot


# TODO put this all into product
api2.update_redis = patched_update_redis
api2.api_log_when_active = api_log_when_active
api2.api_start = api_start
api2.api_fin = api_fin
api2.api_upd = api_upd
# _.send_usp_job = Functions.usp.send_usp_job
