try:
    num = int(input("请输入一个整数:"))
    result = 8/num
    print(result) 

except ValueError:
    print("不能输入字母")

# except ZeroDivisionError:
#     print("不能输入 0 ")
    
except Exception as aa:
    print("未知错误 %s" % aa)

else:
    print("正确时执行")

finally:
    print("都会处理")