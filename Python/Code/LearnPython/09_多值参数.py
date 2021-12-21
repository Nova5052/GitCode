def demo(num,*nums,**person):

    print(num)
    print(nums)
    print(person)


gl_tuple=(2,3,4,5)
gl_dic={"name":"小明","age":18}
# demo(1,2,3,4,name="小明",age=18)
# demo(1,gl_tuple,gl_dic)
demo(1,*gl_tuple,**gl_dic)