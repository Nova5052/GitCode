# 第一个注释
print('hello world')  # 这是第二个注释

"""
print('hello world1')
print('hello world2')
print('hello world3')

"""


# print('hello world4')
#
# name = "xiao ming"
# age = 18
# high = 1.7356
# weight = 50
# scale = 25
# print("姓名:%s 年龄:%d 身高:%.03f 体重:%05d 比例:%.2f%%" % (name, age, high, weight, scale))
#

def age_function(age, num):
    """

    :param age:
    :param num:
    """
    age = 18
    num = 20
    if age > 18 and num > 10:
        print("111")
        print("222")
    else:
        print("33333")
        print("555")


age_function(10, 20)
