import redis

# connect to local redis instance
r = redis.Redis(host = "localhost", port = 6379, db = 0) # db = 0 defines data number, 0 by default


