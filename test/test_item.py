from fastspider.item.item import Item

item = Item()
item.title = "123"
item.src = "http://dddd"

print(item.title)
print(item.src)


class MyItem(Item):

	def __init__(self, title, src):
		self.title = title
		self.src = src


i = MyItem("121212", "sdasdsd")
print(i.title)
print(i.src)
print(i.table_name)
