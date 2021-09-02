import redis

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=1, password="", decode_responses=True)

pipeline = r.pipeline()
pipeline.multi()

pipeline.execute_command("ZADD", "test", 30, "wang")
a = pipeline.execute()
print(a)
print(type(a))
