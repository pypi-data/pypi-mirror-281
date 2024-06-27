from wifi.cspui import tools as t
from devapp.app import app
from operators.ctrl import hpstreams
import json


class streaming:
    def on_vis(req):
        S = req['S']
        cpeid = S.cpe
        if not cpeid:
            return  # different UI

        def _on_nxt_live(msg, S=S):
            dom = t.div('streaming', json.dumps(msg['payload']))
            app.info('pushing htmx', dom=dom)
            S.send(dom)

        h = {'nxt': _on_nxt_live, 'sid': S.id}
        # p = {'scn': 'lightscan', 'cpeid': cpeid, 'chn': 'local', 'dt': '5000'}
        p = {'scn': 'lightscan', 'chn': 'local', 'dt': '10000', 'ident': 'status'}
        job = {'action': 'status', 'params': p, 'handler': h}
        cancel = hpstreams.listen(job)
        S.subs['streaming'] = cancel

        # subscribe to streams
        return t.div('streaming', t.div('', 'hi there'))

    def on_invis(req):
        cancel = req['S'].subs.get('streaming')
        cancel() if cancel else 0
        # unsubscribe fom streams
        return t.div('streaming', t.div('', '...and gone. magic'))


t.components.append(streaming)
