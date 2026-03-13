# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

# 练习1：学生成绩排序
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
    {"name": "赵六", "score": 92}
]

# 要求：
# 1. 按分数从高到低排序（分数相同的按姓名排序）

# result = sorted(students, key=lambda x: x["score"])
# print(result)

result1 = sorted(students, key=lambda x: (-x["score"], x["name"]))
print("第1题结果：", result1)

# 2. 只取出分数大于80的学生，按分数排序
filtered = [s for s in students if s["score"] > 80]
result2 = sorted(filtered, key=lambda x: x["score"], reverse=True)
print("第2题结果：", result2)

# 或者 filtered = list(filter(lambda x: x["score"] > 80, students))
# result2 = sorted(filtered, key=lambda x: x["score"], reverse=True)
