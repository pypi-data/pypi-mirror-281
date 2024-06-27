from wifi.cspui import tools as t
from devapp.app import app
from operators.ctrl import hpstreams
import json

P = t.partial


def on_nxt_live(msg, S):
    dom = t.div('live_stats', msg['payload']['content'])
    app.info('pushing htmx', dom=dom)
    S.send(dom)


class live_stats:
    def on_vis(req):
        S = req['S']
        cpeid = S.cpe
        if not cpeid:
            return  # different UI

        h = {'nxt': P(on_nxt_live, S=S), 'sid': S.id}
        # p = {'scn': 'lightscan', 'cpeid': cpeid, 'chn': 'local', 'dt': '5000'}
        # p = {'scn': 'lightscan', 'chn': 'local', 'dt': '10000', 'ident': 'status'}
        # job = {'action': 'status', 'params': p, 'handler': h}
        p = {'filename': '/tmp/test.html', 'push_content': True, 'interval': 1}
        stream = {'action': 'ax.src.file_watch', 'params': p, 'handler': h}
        cancel = hpstreams.listen(stream)
        S.subs['live_stats'] = cancel

        # subscribe to streams
        return t.div('live_stats', t.div('', 'requesting stream...'))

    def on_invis(req):
        cancel = req['S'].subs.get('live_stats')
        cancel() if cancel else 0
        # unsubscribe fom streams
        return t.div('live_stats', t.div('', '...and gone.'))


t.add_comp(live_stats)
