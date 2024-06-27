from wifi.cspui.tools import span


def fmt_rssi(s, row, table):
    if s == 0:  # lan
        s, c, t = '-', '#444', 'Ethernet (no RSSI)'
    else:
        c, t = (
            (
                '#8bd124',
                "Strong signal: -30 to -50 dBm. This is practically the highest you'll get, typically seen when you're right next to the router.",
            )
            if s > -50
            else (
                'green',
                'Good signal: -50 to -60 dBm. This is usually adequate for most usage scenarios, including streaming and video calls.',
            )
            if s > -60
            else (
                'blue',
                'Fair signal: -60 to -70 dBm. You might start seeing some minor issues at the lower end of this range, especially with more demanding applications.',
            )
            if s > -70
            else (
                'magenta',
                "Weak signal: -70 to -80 dBm. You're likely to encounter noticeable issues with speed and reliability here.",
            )
            if s > -80
            else (
                'red',
                "Very weak signal: -80 to -90 dBm. At this level, you're very likely to experience poor performance. ",
            )
            if s > -90
            else (
                'red',
                'Unusable signal: -90 dBm or lower. Most devices will lose network connection at this level.',
            )
        )
        if s > -50 or s < -90:
            s = '<b>%s</b>' % s
        s = str(s)

    return span('', s, color=c, tooltip=t)


def fmt_band(s, row, table):
    if s == '2':
        return '2.4 GHz'
    if s == '5':
        return '5 GHz'
    return ''


def fmt_ssid(s, row, table, main={'1', '5'}, guest={'2', '6'}):
    if s in main:
        return 'Main'
    if s in guest:
        return 'Guest'
    return s


def fmt_host(s, row, table):
    return f'<span style="width:24rem!important">{s}</span>'


class Hosts:
    class HostName:
        fmt = fmt_host

    class vendor:
        title = 'Vendor'

    class PhysAddress:
        title = 'MAC Address'

    class IPAddress:
        ch = "arrayStringConcat(arraySlice(splitByString(':', toString(IPAddress)), -3), ':')"

    class InterfaceType:
        title = 'Type'

    class band:
        title = 'Band'
        fmt = fmt_band

    class ssid:
        title = 'SSID'
        fmt = fmt_ssid

    class standard:
        title = 'Std'
        ch = "replaceOne(standard, 'IEEE 802.', '')"

    class SignalStrength(int):
        title = 'RSSI'
        fmt = fmt_rssi

    class SNR(int):
        title = 'SNR'

    class LastDataDownlinkRate(int):
        ch = 'round(LastDataDownlinkRate / 2048)'

    class LastDataUplinkRate(int):
        ch = 'round(LastDataUplinkRate / 2048)'

    class ErrorsReceived(int):
        pass

    class ErrorsSent(int):
        pass

    class BytesReceived(int):
        pass

    class BytesSent(int):
        pass

    class PacketsReceived(int):
        pass

    class PacketsSent(int):
        pass

    class Retransmissions(int):
        title = 'Retrans'

    class RetransCount(int):
        title = 'Retrans. Count'
