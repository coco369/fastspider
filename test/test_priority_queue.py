from queue import PriorityQueue


class Test():

	def __init__(self):
		self.priority = 300

	def __lt__(self, other):
		return self.priority < other.priority


queue = PriorityQueue()

for i in range(5):
	t = Test()
	queue.put(t)

print(queue.qsize())
print(queue.get())
