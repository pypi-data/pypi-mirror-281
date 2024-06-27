"""
"""
# FIXME: live demo mode. No pipeline yet, no ch
import json, requests
import time

now = time.time


state_params = [
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
    'Device.DeviceInfo.HardwareVersion',
    'Device.DeviceInfo.Manufacturer',
    'Device.DeviceInfo.ManufacturerOUI',
    'Device.DeviceInfo.MemoryStatus.Free',
    'Device.DeviceInfo.MemoryStatus.Total',
    'Device.DeviceInfo.ModelName',
    'Device.Ethernet.Link.',
    'Device.IEEE1905.AL.NetworkTopology.',
]


def get_to_dict(r):
    res = r['Response']['GetResp']['req_path_results']
    m = {}

    def add(m, pth, params):
        n = {pth + k: params[k] for k in params}
        m.update(n)

    def jobd(k, m):
        for i in k['resolved_path_results']:
            add(m, i['resolved_path'], i['result_params'])

    [jobd(k, m=m) for k in res]
    return m


def state(cpeid):
    r = requests.post(
        f'http://192.168.29.104:57879/v1/{cpeid}/get',
        json.dumps(state_params),
        headers={'Content-Type': 'application/json'},
        timeout=10,
    )
    r = r.text
    if not r or not r[0].strip() == '{':
        return
    r = json.loads(r)
    r = get_to_dict(r)
    return r


if __name__ == '__main__':
    i = 'os::00040E-DC15C8B5911C'
    while 1:
        breakpoint()  # FIXME BREAKPOINT

        r = state(i)
