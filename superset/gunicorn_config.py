workers = 2
worker_class = 'gevent'

bind = '0.0.0.0:8088'
daemon = True
reload = True

timeout = 120
limit_request_line = 0
limit_request_field_size = 0
statsd_host = 'localhost:8125'