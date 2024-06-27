from devapp.app import app
from wifi.cspui.const import Sessions


def send(htmx, S):
    try:
        S.ws.send(htmx)
    except Exception as _:
        return rm_session(S.id)
    if app.log_level < 20:
        app.debug('full payload', htmx=htmx.split('series', 1)[0])
    l = len(htmx)
    if l > 100:
        b = round(l / 1024, 1)
        htmx = htmx[:100] + f'...[{b}kB]'
    app.info('⬇️ htmx ', htmx='\n' + htmx)


class session:
    url = ''

    def __init__(self, id, ws):
        self.id = id
        self.ws = ws
        self.subs = {}

    def cpe(self):
        return self.cpeid

    def send(self, htmx, snd=send):
        return snd(htmx, self)

    def __repr__(self) -> str:
        return f'Session (cpe: {self.cpe()}) [{self.id}]'


def make_session(msg):
    req = msg['payload']
    sid = req['id']
    ws = msg['objs']['src']['ws']
    Sessions[sid] = S = session(sid, ws)
    S.cpeid = msg['payload']['path'].split('/cpeid/', 1)[1]
    app.info('New session', session=S, cpeid=S.cpe())
    return S


def rm_session(sid):
    S = Sessions.pop(sid, 0)
    app.info('removing session', sid=sid, left=len(Sessions))
    if not S:
        return app.warn('Session to rm not found', sid=sid)
    if not S.subs:
        return
    for k, cncl in S.subs.items():
        app.info(f'Unsubscribing {k}')
        cncl()
