
import datetime

x = datetime.datetime.now()
y = datetime.datetime(2020, 1, 1, 0, 0, 0)

delta = x - y

print(delta.total_seconds())