from devapp.app import app
from operators.con.clickhouse import clickhouse

result = clickhouse.get('SELECT * FROM hosts LIMIT 3')
print(result.result_rows)
