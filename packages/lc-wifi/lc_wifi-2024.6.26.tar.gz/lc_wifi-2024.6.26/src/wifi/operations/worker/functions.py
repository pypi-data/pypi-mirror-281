"""
Sample Real Project Custom Functions

Adapt to your needs
"""

from wifi import WiFiFunctions
from ax.utils.ax_tree import AXTree
from wifi.usp.usp import cast
import time
from devapp.app import app


cuts = ['os::E87829-CCKKCNC0N22000005']  # cpe under test
for d in cuts:
    # WiFiFunctions.usp.c_nb_by_epid[d] = 'http://testbed.axiros.hr:10296'
    WiFiFunctions.usp.c_nb_by_epid[d] = 'http://192.168.29.104:57879'

ls_paths = [
    'Device.DeviceInfo.',
    'Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.',
    'Device.X_JOINTELLI_COM_H.Common.MACAddress',
    'Device.IP.Interface.',
]


class Functions(WiFiFunctions):
    class custom:
        class usp:
            class lightscan:
                def params_by_cpeid(id, patched):
                    if id in cuts:
                        return [ls_paths, 0]
                    return patched(id)

                def to_tr181(data, patched):
                    id = data['id']
                    if id in cuts:
                        jointelli_ls_to_tr181(data)
                    else:
                        patched(data)

    def periodic_getter(dt=60):
        while True:
            app.info('Will send next get in', dt=dt)
            time.sleep(dt)
            for cpe in cuts:
                yield {'id': cpe, 'interval': dt, 'type': 'lightscan.get'}


def jointelli_ls_to_tr181(data):
    # --                                                                 "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.Associations": "0",
    # Device.WiFi.Radio.i.AutoChannelEnabled                             "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.AutoChannelEnabled": "1",
    # Device.WiFi.Radio.i.OperatingChannelBandwidth                      "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.Bandwidth": "auto",
    # --                                                                 "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.Channel": "0",
    # Device.WiFi.Radio.i.Enabled                                        "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.Enable": "1",
    # --                                                                 "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.Hidden": "0",
    # Device.WiFi.Radio.i.OperatingStandards                             "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.NetworkMode": "b/g/n/ax",
    # Device.WiFi.Radio.i.Channel                                        "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.OperatingChannel": "7",
    # --                                                                 "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.Passwd": "********",
    # Device.WiFi.SSID.i.SSID                                            "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host.i.SSID": "5G CPE_09C3_2.4G",
    # Device.WiFi.AccessPoint.i.Security.ModeEnabled                     "Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID.Host..SecurityMode": "WPA2-PSK/WPA3-SAE"
    ret = {}
    m = {}
    ip = {}
    max, is_max = 0, ''
    d = data['props']
    for k in d:
        if k.startswith('Device.X'):
            m[k] = d[k]
        if k.startswith('Device.IP'):
            ip[k] = d[k]
            if k.endswith('BytesReceived'):
                if int(d[k]) > max:
                    max = int(d[k])
                    is_max = k.split('.')[3]
        else:
            v = cast(d[k]) if not k.endswith('SpecVersion') else d[k]
            ret[k] = v
    ip = AXTree(ip)
    if is_max != '1':
        # we expect WANT iface on 1
        o = ip['Device']['IP']['Interface'].pop('1')
        n = ip['Device']['IP']['Interface'].pop(is_max)
        ip['Device']['IP']['Interface']['1'] = n
        ip['Device']['IP']['Interface'][is_max] = o

        for k, v in ip.iter_leaf_items():
            ret[k] = v

    mac = d['Device.X_JOINTELLI_COM_H.Common.MACAddress']
    mac = f'{mac[:2]}-{mac[2:4]}-{mac[4:6]}-{mac[6:8]}-{mac[8:10]}-{mac[10:12]}'
    m = AXTree(m)['Device']['X_JOINTELLI_COM_H']['DeviceMonitorRouter']['WiFiSSID']

    app.debug('Remapping', payload=m)
    t = AXTree({})
    rad1 = t['Device.WiFi.Radio.1'] = AXTree()
    rad5 = t['Device.WiFi.Radio.5'] = AXTree()

    def bl(k):
        return True if str(k).lower() in {'1', 'true'} else False

    P = 'Device.X_JOINTELLI_COM_H.DeviceMonitorRouter.WiFiSSID'
    for r, idx in [[rad1, '1'], [rad5, '2']]:
        h = m['Host'][idx]
        r['orig_node'] = P + '.Host.' + idx
        r['orig_AutoChannelEnable'] = 'AutoChannelEnabled:int'
        r['Enable'] = e = bl(h['Enable'])
        r['Status'] = 'Up' if e else 'Down'
        r['OperatingStandards'] = h['NetworkMode'].replace('/', ',')
        r['Channel'] = int(h['OperatingChannel'])
        bw = h['Bandwidth']
        r['OperatingChannelBandwidth'] = {'auto': 'Auto'}.get(bw, bw)
        r['AutoChannelEnable'] = bl(h['AutoChannelEnabled'])
        r['OperatingFrequencyBand'] = {'1': '2.4GHz', '2': '5GHz'}.get(idx)

    ssid1 = t['Device.WiFi.SSID.1'] = AXTree()
    ssid2 = t['Device.WiFi.SSID.2'] = AXTree()
    ssid5 = t['Device.WiFi.SSID.5'] = AXTree()
    ssid6 = t['Device.WiFi.SSID.6'] = AXTree()
    for r, n, idx in [
        [ssid1, 'Host', '1'],
        [ssid5, 'Host', '2'],
        [ssid2, 'Guest', '1'],
        [ssid6, 'Guest', '2'],
    ]:
        h = m[n][idx]
        r['orig_node'] = '.'.join([P, n, idx])
        r['SSID'] = h['SSID']
        r['Enable'] = bl(h['Enable'])
        r['BSSID'] = mac.rsplit('-', 1)[0] + f'-0{idx}'
        r['LowerLayers'] = 'Device.WiFi.Radio.' + ('1' if idx == '1' else '5')

    ap1 = t['Device.WiFi.AccessPoint.1'] = AXTree()
    ap2 = t['Device.WiFi.AccessPoint.2'] = AXTree()
    ap5 = t['Device.WiFi.AccessPoint.5'] = AXTree()
    ap6 = t['Device.WiFi.AccessPoint.6'] = AXTree()
    for r, n, idx, ref in [
        [ap1, 'Host', '1', '1'],
        [ap5, 'Host', '2', '5'],
        [ap2, 'Guest', '1', '2'],
        [ap6, 'Guest', '2', '6'],
    ]:
        h = m[n][idx]
        r['orig_node'] = '.'.join([P, n, idx])
        sec = h.get('SecurityMode', 'open')
        sec = 'None' if sec == 'open' else sec
        r['Security.ModeEnabled'] = sec
        r['Enable'] = bl(h['Enable'])
        r['SSIDReference'] = 'Device.WiFi.SSID.' + ref
    app.debug('Remapped', payload=t)
    for k, v in t.iter_leaf_items():
        ret[k] = v
    ret['Device.Ethernet.Link.1.MACAddress'] = mac
    ret['Device.LocalAgent.Controller.1.MTP.1.Enable'] = True
    ret['Device.LocalAgent.Controller.1.MTP.1.Protocol'] = 'MQTT'
    data['props'] = ret
    data['cap_fullscans'] = False


#
# def light_scan_params_by_epid(data):
#     breakpoint()  # FIXME BREAKPOINT
#
#
# def light_scan_result_to_tr181(data):
#     breakpoint()  # FIXME BREAKPOINT
#
#
# Functions.usp.light_scan_params_by_epid = light_scan_params_by_epid
# Functions.usp.light_scan_result_to_tr181 = light_scan_result_to_tr181
