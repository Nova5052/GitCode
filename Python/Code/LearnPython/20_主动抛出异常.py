def input_pwd():
    pwd = input("请输入密码:")
    if len(pwd) > 8:
        return pwd
    else:
        ex1 = Exception("密码长度不够")
        raise ex1


try:
    print(input_pwd())
except Exception as ex:
    print(ex)
