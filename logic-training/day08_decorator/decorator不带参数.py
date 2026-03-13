# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

def print_start_end(func):
    def wrapper(*args, **kwargs):
        print("开始执行")
        result = func(*args, **kwargs)
        print("结束执行")
        return result

    return wrapper


@print_start_end
def test():
    print("hello")


# @print_start_end等价于test = print_start_end(test)

test()
