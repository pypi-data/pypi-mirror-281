from enum import unique
from operators.core import ax_core_ops
from devapp.tools import read_file, dir_of, exists, os
from devapp.app import app
import json
from wifi.cspui import tools as t
from wifi.cspui import session

# those autoregister at t.components:
# from wifi.cspui.comps import live_stats  # noqa
from wifi.cspui.comps import charts  # noqa
from wifi.cspui.comps import client_stats  # noqa

# from wifi.cspui.comps import quotes  # noqa
from wifi.cspui.const import Sessions, HxEvts

from wifi.cspui.tools import App, div, script, id_ui, ls, Components, pjoin, lsjoin


here = dir_of(__file__)
send = session.send


def symlink_static_files(fn_functions):
    d_proj = dir_of(dir_of(fn_functions))
    fn = d_proj + '/ui_static_files'
    if exists(fn):
        return
    app.info(f'symlinking ui_static_files to {fn}')
    os.symlink(here + '/ui_static_files', fn)


T = t.axui
T.constants()
T.local_tools()
T.vis_checker()
T.local_bus()

# monkey path the angular posting:
# f = """
# (function (send) {
#   XMLHttpRequest.prototype.send = function (data) {
#     var self = this;
#     setTimeout(function () {
#       send.call(self, data);
#     }, 500); // delay of 5 seconds
#   };
# })(XMLHttpRequest.prototype.send);
#
#
#
# """
# App.js += [f]
#
# Fastest is the local bus method, i.e. we get an HxEvt:
# TComps = lsjoin(
#     div('streaming', '%(client_stats)s'),
#     # div('hxradiocharts', '%(radio_charts)s'),
#     # div('extra_1', '%(quotes)s'),
# )
# Comps = TComps % Components  # magic. gd on Components
# Comps = ''
# Comps = """
# <script>axui.bus('streaming', {})</script>
#  ""
Comps = ''
App.js += ['console.log("✨ UI in the DOM")']
App.js = lsjoin(App.js, uniq=1)
App.css = lsjoin(App.css, uniq=1)
App.dom = lsjoin(App.dom, uniq=1)


def app_init_hx(c=[0]):
    if not c[0]:
        css = lsjoin('<style>', App.css, '</style>')
        app = lsjoin(css, App.dom, script(id_ui + '-js', App.js))
        # c[0] = div('', app + Comps)  # http-get has target id
        # Sending these here again, for dev reload:
        # c[0] = lsjoin(
        #     div(id_ui, app + Comps),
        #     #div('hxcharts', '', hx_trigger='load'),
        # )

        c[0] = app  # div(id_ui, app + Comps)
    return c[0]


def bottle_ui(req, msg):
    hx = req.get('raw')
    if not hx:
        return

    if hx == 'connect':
        S = req['S'] = session.make_session(msg)
        app.info('connect')
        App = app_init_hx()
        msg = div(id_ui, App)  # + '<script>alert("foo");debugger</script>')
        # app.info('sending', app=msg)
        return session.send(msg, S)

    if hx == 'closed':
        return session.rm_session(req['id'])

    S = Sessions.get(req['id'])
    hx = req['hx'] = json.loads(hx)
    req['S'] = S

    _ = hx['HEADERS']
    cbid = _['HX-Trigger']
    S.url = _['HX-Current-URL']

    cb = HxEvts.get(cbid)
    if not cb:
        return app.warn('No callback registered', id=cbid, json=hx)

    app.info(f'⬆️ {cbid}', hx=hx)
    r = cb(req)
    if isinstance(r, str) and r:
        send(r, req['S'])


def ui(req, msg):
    raw = req['raw']
    if raw is None:
        return

    if raw == 'connect':
        S = session.make_session(msg)
        app.info('connect')
        App = app_init_hx()
        msg = div(id_ui, App)  # + '<script>alert("foo");debugger</script>')
        # app.info('sending', app=msg)
        return session.send(msg, S)

    if raw == 'closed':
        app.warn('session closed', id=req['id'])
        return session.rm_session(req['id'])

    S = Sessions.get(req['id'])
    hx = req['hx'] = json.loads(raw)
    req['S'] = S

    _ = hx['HEADERS']
    cbid = _['HX-Trigger']
    S.url = _['HX-Current-URL']

    cb = HxEvts.get(cbid)
    if not cb:
        return app.warn('No callback registered', id=cbid, json=hx)

    app.info(f'⬆️ {cbid}', hx=hx)
    r = cb(req)
    if isinstance(r, str) and r:
        send(r, req['S'])


class Functions(ax_core_ops):
    class csp:
        ui = ui  # the only custom func in NR
