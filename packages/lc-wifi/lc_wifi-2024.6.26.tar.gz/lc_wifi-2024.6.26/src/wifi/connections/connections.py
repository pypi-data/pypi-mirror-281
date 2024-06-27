from operators.con import con, add_connection, redis, http, kafka, elastic, clickhouse
from wifi.connections import elastic as es
from wifi.connections import clickhouse_rrd as rrd_ch
from wifi.connections import clickhouse_elastic as elastic_ch
from wifi.connections import clickhouse_hosts as hosts_ch
from wifi.connections import clickhouse_pme as pme_ch
from wifi.connections import clickhouse_rec as rec_ch
from wifi.connections import clickhouse_inform_stats as inform_stats_ch

# define available connection ops (e.g. "con.redis")
allcons = redis.redis, http.http, kafka.kafka, elastic.elastic, clickhouse.clickhouse
[add_connection(cls, cls.__name__) for cls in allcons]
add_connection(http.http, 'http_bulk_data', req_conf=True)
con.elastic.con_attributes = es.Attrs
con.clickhouse.rrd_con_attributes = rrd_ch.Attrs
con.clickhouse.hosts_con_attributes = hosts_ch.Attrs
con.clickhouse.elastic_con_attributes = elastic_ch.Attrs
con.clickhouse.pme_con_attributes = pme_ch.Attrs
con.clickhouse.rec_con_attributes = rec_ch.Attrs
con.clickhouse.inform_stats_con_attributes = inform_stats_ch.Attrs
