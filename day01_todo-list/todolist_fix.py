# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22
# 1. 数据存储（最简单的内存存储）

tasks = []  # 任务列表
next_id = 1  # 下一个ID


# 2. 添加任务（第一个要实现的函数）
def add_task(title):
    """添加新任务"""
    global next_id

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    next_id += 1
    print(f"✅ 添加任务：{title}")
    return task


# 3. 查看任务
def list_tasks():
    """列出所有任务"""
    if not tasks:
        print("📭 还没有任务")
        return

    print("\n📋 我的任务清单：")
    for task in tasks:
        status = "✅" if task["completed"] else "⬜"
        print(f"{task['id']}. {status} {task['title']}")


# 4. 标记任务完成
def complete_task(task_id):
    """标记任务完成"""
    found = False  # 先假设没找到

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            print(f"✅ 任务 {task_id} 已完成")
            found = True
            break  # 找到了就退出循环

    if not found:  # 如果没找到
        print(f"❌ 任务 {task_id} 不存在")


# 5. 删除任务
def delete_task(task_id):
    """删除任务"""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            print(f"✅ 已删除任务：{deleted_task['title']}")
            return

    print(f"❌ 任务 {task_id} 不存在")


if __name__ == "__main__":
    add_task("学习python")
    add_task("学习英语")
    add_task("给朋友买生日礼物")
    list_tasks()
    complete_task(1)
    complete_task(4)
    delete_task(3)
    print("删除前：", [t["title"] for t in tasks])
    delete_task(2)  # 调用你的函数
    print("删除后：", [t["title"] for t in tasks])
