info_tuple = ("zhangsan", 19, 1.75)
# print(type(info_tuple))
# print(info_tuple[0])
# print(info_tuple.index("zhangsan"))
# print(info_tuple.count("zhangsan"))
# print(len(info_tuple))

# str1 = '%s 年龄是:%d 身高是:%.2f' % info_tuple
# print(str1)

info_list=list(info_tuple)
print(type(info_list))
info2_tuple=tuple(info_list)
print(type(info2_tuple))