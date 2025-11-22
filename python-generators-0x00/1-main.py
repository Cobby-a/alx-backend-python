from itertools import islice
module = __import__('0-stream_users')

for user in islice(module.stream_users(), 6):
    print(user)