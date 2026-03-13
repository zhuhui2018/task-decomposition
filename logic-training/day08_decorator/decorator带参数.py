# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

# def say_before(message):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             print(f"{message}")
#             result = func(*args, **kwargs)
#             return result
#
#         return wrapper
#
#     return decorator
#
#
# @say_before("我要开始表演了")
# def test():
#     print("hello")
#
#
# test()

#############################

# def repeat(n):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             # 你的代码：循环 n 次调用 func
#             for i in range(n):
#                 func()
#         return wrapper
#     return decorator
#
#
# @repeat(3)
# def say():
#     print("hello")
#
#
# say()

#################################

# import time
#
#
# def timer(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         print(end_time - start_time)
#         return result
#
#     return wrapper
#
#
# @timer
# def add(a, b):
#     time.sleep(0.5)
#     return a + b
#
#
# result = add(3, 5)
# print(f"结果：{result}")

############################

def require_role(role):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            # 如果 user 的 role 等于要求的 role，执行函数
            # 否则打印 "无权限"
            if role == user["role"]:
                func(user, *args, **kwargs)
            else:
                print("没有权限")
        return wrapper
    return decorator


@require_role("admin")
def delete_user(user, user_id):
    print(f"用户 {user_id} 已删除")


# 测试
admin = {"name": "阿黄", "role": "admin"}
guest = {"name": "访客", "role": "guest"}

delete_user(admin, 1001)  # 应该成功
delete_user(guest, 1002)  # 应该提示无权限
