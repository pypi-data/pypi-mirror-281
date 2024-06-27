from devapp.tools import read_file, dir_of
from pathlib import Path
from functools import partial
import re
from devapp.app import app
from wifi.cspui.const import HxEvts, App

here = dir_ui = dir_of(__file__)

id_ui = '🟢ui'


comp_by_id = {}


class Components:
    def __getitem__(self, id):
        c = comp_by_id[id]
        load = g(c, 'on_load', None)
        if load:
            topic = id + '-loaded'
            HxEvts[topic] = load
            App.js += [f'axui.bus("{topic}")']

        r = div(id, '')
        if g(c, 'on_vis', None):
            r = div(id + '-vis', r)
            App.js += [f"axui.vis_check('{id}')"]
            if not g(c, 'on_invis', None):
                c.on_invis = lambda _: ''
        return r


Components = Components()

g = getattr
p = partial


ls = '\n'


def render(T, **kw):
    return T % kw


def id(prefix):
    def prefixed(s, p=prefix):
        return p + '-' + s

    return prefixed


def add_comp(comp):
    id = g(comp, 'id', comp.__name__)
    comp_by_id[id] = comp


def src(fn, dir=Path(dir_ui)):
    if dir is True:
        # we always want gf to work, i.e. will have ../../file as fn
        # dir = True will strip the dots and work from ui dir
        fn = fn.split('/', 1)[1]
        dir = Path(here)
    path = Path(dir) / fn
    return path.read_text().split('begin_archive', 1)[0]


def pjoin(l, pre, post=None):
    if post is None:
        i = pre
        post = ''
    else:
        i = post + pre
    return pre + i.join(l) + post


def lsjoin(*s, uniq=False):
    if len(s) == 1 and not isinstance(s[0], str):
        s = s[0]
    if uniq:
        s = list(dict.fromkeys(s))
    return pjoin(s, ls)


def trs(rows):
    return pjoin(rows, '<tr>', '</tr>')


elmt_alias = {
    'color': 'style="color:%s"',
    'glyph': 'class="glyphicon glyphicon-%s"',
    'tooltip': 'title="%s" data-toggle="tooltip"',
    'cls': 'class="%s"',
}


def elmt_attr(k, v, a=elmt_alias):
    try:
        return a[k] % v
    except Exception as _:
        pass
    k = k.replace('_', '-')
    va = f'"{v}"'
    if k.startswith('hx-'):
        va += ' ws-send'
    return f'{k}={va}'


def elmt_attrs(attrs):
    a = ' '.join([elmt_attr(k, v) for k, v in attrs.items()])
    if a:
        a = ' ' + a
    return a


def js_tmpl_to_py_tmpl(s):
    """we want synt.correct js templates, with %()s phs.
    When those are e.g. data: %(data)s we require apos in js.
    We use `` for those, since prettifier might convert ' to "
    Examples: In highcharts js templates.

    "... `%${data}s` ..." -converted to-> "... %(data)s ..."
    """
    return re.sub(r'`%\$\{(.+?)\}s`', r'%(\1)s', s)


def js_tmpl(fn, dir=Path(dir_ui)):
    return js_tmpl_to_py_tmpl(src(fn, dir))


# <thead id=foo hx-trigger="click" ws-send hx-vals="js:{clickedElement: event.target.innerText}">
def autoid(c=[0]):
    c[0] += 1
    return 'axui-%s' % c[0]


def handle_listen_attr(id, attrs):
    l = attrs.pop('listen', None)
    if isinstance(l, dict):
        l = l.get(id)
    if not l:
        return
    if not id:
        id = autoid()
    if isinstance(l[0], str):
        l = [l]
    evts = l
    for l in evts:
        trigger = l[0]
        cb = l[1]
        w = ','.join([f'{i}:event.target.{i}' for i in l[2:]])
        want = (',' + w) if w else ''
        attrs['hx_vals'] = f'js:{{id:event.target.id{want}}}'
        attrs['hx_trigger'] = trigger
        HxEvts[id] = cb


def elmt(typ, id, body, **attrs):
    handle_listen_attr(id, attrs)

    if not isinstance(body, str):
        body = '\n'.join(body)
    if id:
        id = ' id="%s"' % id
    s = f'<{typ}{id}{elmt_attrs(attrs)}>\n{body}\n</{typ}>'
    return s


def thead(id, body, **attrs):
    return elmt('thead', id, body, **attrs)


def div(id, body, **attrs):
    return elmt('div', id, body, **attrs)


def span(id, body, **attrs):
    return elmt('span', id, body, **attrs)


def script(id, body, **kw):
    return '\n' + elmt('script', id, body, **kw) + '\n'


def run_js(js):
    """This script id is always in the dom -> multipurpose execution of stuff
    e.g. remove toggle class, add a func to uitools...
    """
    return script(id_ui + '-js', js)


def css_cls(do, cls, eid):
    return run_js(f'axui.byid("{eid}")?.classList.{do}("{cls}")')


class axui:
    def constants():
        App.js += ['axui.id_ui="%s"' % id_ui, 'axui.close_cleared=false']

    def local_tools():
        App.js += [src('js/local_tools.js')]

    def vis_checker():
        App.js += [src('js/vis_checker.js')]

        def on_vis_change(req):
            evt = req['hx']['local_evt']
            vis = evt.get('vis')
            app.info('Viz event', el=evt['id'], vis=vis)
            c = comp_by_id[evt['id']]
            return c.on_vis(req) if vis else c.on_invis(req)

        HxEvts['vis-change'] = on_vis_change

    def local_bus():
        def handle_local_evt(req):
            evt = req['hx']['local_evt']
            typ = evt.get('typ')
            if typ:
                cb = HxEvts.get(typ)
                if cb:
                    return cb(req)
            app.warn('Unhandled local evt', evt=evt)

        App.js += [src('js/local_bus.js')]
        _ = 'js:{local_evt:axui.cur_event}'
        id = id_ui + '-local-evts'
        App.dom += [div(id, '', hx_trigger='click', hx_vals=_)]
        HxEvts[id] = handle_local_evt
