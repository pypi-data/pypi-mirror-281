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
    id                  = ['id',               str           , ""   , True]
    ts                  = ['ts',               C.to_date_time, 0]

    name                = ["name",             str, ""   ]
    source              = ["source",           str, ""   ]
    action              = ["action",           str, ""   ]
    operation           = ["operation",        str, ""  ]
    relation            = ["relation",         str, ""   ]
    calculated_value    = ["calculated_value", str, ""   ]
    moving_average      = ["moving_average",   str, ""   ]
    threshold           = ["threshold",        str, ""   ]
    description         = ["description",      str, ""   ]
    uid                 = ["elastic_id",       str, ""   ]
    enforce             = ["enforce",          all_bool, False   ]
    title               = ["title",            str, ""   ]

    # fmt:on

