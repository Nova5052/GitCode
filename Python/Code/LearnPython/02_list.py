name_list = ["张三", "李四", "王五"]

print(name_list[1])
print((name_list.index("李四")))
name_list[0] = "zhang san"
name_list.append("wang xiao er")
name_list.insert(1, "小妹妹")
name_list.extend(["h1", "h2"])

# name_list.remove("王五")
# name_list.pop()
# name_list.pop(2)
# name_list.clear()

for name in name_list:
    print("我的名字是:%s" % name)

print(name_list)
