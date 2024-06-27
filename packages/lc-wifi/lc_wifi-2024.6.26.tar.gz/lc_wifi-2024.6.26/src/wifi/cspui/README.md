# Usage

## AXESS

Put this anywhere into the old CSP:

      fetch("/lc-csp/csp/assets/static/bootstrap.js")
        .then((response) => response.text())
        .then((script) => {
          console.log("XTRM", script);
          new Function(script)();
        });


## nginx

including also redir to low code node red (optional):

      upstream lc_wifi {
              server 127.0.0.1:1880;
      }

      upstream lc_csp {
              server 127.0.0.1:3800;
      }

        location ~ ^/lc-wifi(/?)(.*) {
            proxy_pass http://lc_wifi/$2;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location ~ ^/lc-csp(/?)(.*) {
              proxy_pass http://lc_csp/$2;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_http_version 1.1;
              proxy_set_header Upgrade $http_upgrade;
              proxy_set_header Connection "upgrade";
              proxy_set_header Host $host;
              proxy_read_timeout 86400;
          }


## static files

    (base) axwifi@axwifi-aio:~/axwifi/ui_static_files/static$ ll
    drwxr-xr-x  5 axwifi axwifi 4096 Jun 10 03:33 .
    drwxr-xr-x  3 axwifi axwifi 4096 Jun  8 13:27 ..
    lrwxrwxrwx  1 axwifi axwifi   32 Jun 10 03:31 bootstrap.js -> ../../conf/cspui/js/bootstrap.js
    drwxr-xr-x  3 axwifi axwifi 4096 Jun  5 10:26 htmx.org
    drwxr-xr-x 10 axwifi axwifi 4096 Apr 16 10:12 kendo
    drwxr-xr-x  3 axwifi axwifi 4096 Jun  5 10:26 rxjs



## worker flags


    --csp_url=http://127.0.0.1:3800/csp?d_assets=ui_static_files&closed_msg=1
    --clickhouse_url=clickhouse://admin:xxxxx@be1-internal:8123?database=axwifi -ll=10

usp controller currently hardcoded

## functions.py

```python
from wifi.cspui import index as csp

from operators.con import add_connection, http, clickhouse

add_connection(http.http, 'csp')
add_connection(clickhouse.clickhouse, 'clickhouse')


class Functions(csp.Functions):
    pass

```

## flow

```javascript
[
    {
        "id": "263e1d8852dd5652",
        "type": "ax-src",
        "z": "f84898ee652a9107",
        "name": "con.csp.request",
        "label": "",
        "async_timeout": 0,
        "deep_copy": false,
        "primary": false,
        "kw": "{}",
        "outputs": 1,
        "x": 160,
        "y": 80,
        "wires": [
            [
                "d5eacb363a5ec2c9"
            ]
        ]
    },
    {
        "id": "d5eacb363a5ec2c9",
        "type": "ax-op",
        "z": "f84898ee652a9107",
        "name": "csp.ui",
        "label": "",
        "async_timeout": 0,
        "deep_copy": false,
        "primary": false,
        "kw": "{}",
        "outputs": 1,
        "x": 370,
        "y": 80,
        "wires": [
            [
                "434e743b885b7dd6"
            ]
        ]
    },
    {
        "id": "434e743b885b7dd6",
        "type": "ax-snk",
        "z": "f84898ee652a9107",
        "name": "ax.noop",
        "label": "",
        "async_timeout": 0,
        "deep_copy": false,
        "primary": false,
        "kw": "{}",
        "outputs": 0,
        "x": 540,
        "y": 80,
        "wires": []
    }
]

```
