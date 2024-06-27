#!/usr/bin/env python
"""
writes to clickhouse
"""
# import urllib3

# urllib3.disable_warnings()

import os


# import redis, json
import operators.con.clickhouse as C
from operators.con.clickhouse import byte, perc, short, long, autoch, all_bool

env = os.environ

# fmt: off
client_mac      = lambda client: client['vendor']
client_rssi     = lambda client: client['SignalStrength']
client_standard = lambda client: client['OperatingStandard']
client_downrate = lambda client: client['LastDataDownlinkRate']

def security(r):
    return '%s:%s' % (
        r.get('EncryptionMode', 'NoEncr'),
        r.get('ModeEnabled', 'Not Enabled'),
    )

C.types.update(
    {
        autoch:          'Bool',
        client_rssi:     'Int16',
        client_standard: 'String',
        client_downrate: 'UInt64',
        client_mac:      'String',
        security:        'String',
        'scan_dt':       'UInt32',
    }
)

DI = 'DeviceInfo'

class Attrs:
    """Clickhouse Parameters Definitions"""

    # for data types, please refer to https://clickhouse.com/docs/en/sql-reference/data-types
    # use Bool, String, DateTime, UInit32, UInt64, Point
    # no default -> omit if missing
    # fmt: off
    # name                     = ['place.in.tree'                  , type          , default, is_db_index]

    # Note: cpeid and ts will get values automatically
    id                   = ['id',                   str, ''   , True]
    ts                   = ['ts',                   C.to_date_time, 0]

    AssociatedDevice     = ['AssociatedDevice',     str, ''   ]
    HostName             = ['HostName',             str, ''   ]
    InterfaceType        = ['InterfaceType',        str, ''   ]
    Active               = ['Active',               all_bool, False  ]
    PhysAddress          = ['PhysAddress',          str, ''   ]
    IPAddress            = ['IPAddress',            str, ''   ]
    Alias                = ['Alias',                str, ''   ]
    vendor               = ['vendor',               str, ''   ]
    hindex               = ['hindex',               str, ''   ]
    DeviceID             = ['DeviceID',             str, ''   ]
    ModelName            = ['ModelName',            str, ''   ]
    Mode                 = ['Mode',                 str, ''   ]
    SignalStrength       = ['SignalStrength',       short, 0 ]
    LinkAvailability     = ['LinkAvailability',     short, 0 ]
    LastDataUplinkRate   = ['LastDataUplinkRate',   long, 0  ]
    LastDataDownlinkRate = ['LastDataDownlinkRate', long, 0  ]
    ParentNodeID         = ['ParentNodeID',         str, ''   ]
    standard             = ['standard',             str, ''   ]
    Layer1Interface      = ['Layer1Interface',      str, ''   ]
    is_meshed            = ['is_meshed',            bool, False   ]
    mesh_role            = ['mesh_role',            str, ''   ]

    # Clients Statistics
    BytesReceived        = ['Stats.BytesReceived',        long, 0  ]
    BytesSent            = ['Stats.BytesSent',            long, 0  ]
    PacketsReceived      = ['Stats.PacketsReceived',      long, 0  ]
    PacketsSent          = ['Stats.PacketsSent',          long, 0  ]
    ErrorsReceived       = ['Stats.ErrorsReceived',       long, 0  ]
    ErrorsSent           = ['Stats.ErrorsSent',           long, 0  ]
    RetransCount         = ['Stats.RetransCount',         long, 0  ]

    OperatingStandard    = ['OperatingStandard',          str,  '' ]
    Retransmissions      = ['Retransmissions',            int,  0  ]
    Noise                = ['Noise',                      int,  0  ]
    SNR                  = ['SNR',                        int,  0  ]

    band                 = ['band',                       str, ''  ]
    ssid                 = ['ssid',                       str, ''  ]

    # fmt:on

