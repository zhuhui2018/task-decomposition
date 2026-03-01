# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22
# 1. 数据存储（最简单的内存存储）
import json
from datetime import datetime


# ===== 文件操作 =====

def load_data():
    """从文件加载数据"""
    try:
        with open("todo.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": [], "next_id": 1}


def save_data(data):
    """保存数据到文件"""
    with open("todo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 2. 添加任务（第一个要实现的函数）
def add_task(data):
    """添加新任务"""
    next_id = data["next_id"]
    priority = input("请输入优先级（1.高 2.中 3.低）：")
    if priority == "1":
        priority = "高"
    elif priority == "2":
        priority = "中"
    elif priority == "3":
        priority = "低"
    else:
        priority = "中"

    title = input("请输入任务名称：")

    last_date = input("请输入截止日期，格式为YYYY-MM-DD：")
    if not last_date:
        last_date = datetime.now().strftime("%Y-%m-%d")

    category = input("请输入任务分类(学习/工作/生活/其他)：")
    created_date = datetime.now().strftime("%Y-%m-%d")

    task = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "deadline": last_date,
        "category": category,
        "completed": False,
        "created_at": created_date
    }

    data["tasks"].append(task)
    data["next_id"] += 1
    print(f"✅ 添加任务：{title}")
    return data


def sort_by_priority(tasks):
    """按优先级排序（高 > 中 > 低）"""

    def get_priority_weight(task):

        if task["priority"] == "高":
            return 3
        elif task["priority"] == "中":
            return 2
        else:
            return 1

    return sorted(tasks, key=get_priority_weight, reverse=True)


def get_today_tasks(data):
    """获取今日任务（截止日期是今天）"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 第2步：创建一个空列表，存放今日任务
    today_tasks = []

    # 第3步：遍历所有任务
    for task in data["tasks"]:
        if task["deadline"] == today:
            today_tasks.append(task)
    return today_tasks


def show_today_tasks(data):
    """显示今日任务"""

    today_tasks = get_today_tasks(data)

    # 第2步：如果没有今日任务，提示并返回
    if not today_tasks:
        print("📭 今天没有待办任务")
        return

    # 第3步：按优先级排序（复用之前的排序函数）
    sorted_tasks = sort_by_priority(today_tasks)

    # 第4步：打印表头
    print("\n📋 今日任务")
    print("=" * 60)
    print(f"{'ID':<4} {'状态':<2} {'标题':<20} {'优先级':<4} {'截止日期':<12} {'分类':<6}")
    print("-" * 60)

    # 第5步：遍历显示
    for task in sorted_tasks:
        status = "✅" if task["completed"] else "⬜"
        print(
            f"{task['id']:<4} {status:<2} {task['title']:<20} {task['priority']:<4} {task['deadline']:<12} "
            f"{task['category']:<6}")

    print("=" * 60)
    print(f"今日共：{len(today_tasks)}个任务")


def show_all_tasks(data):
    """显示所有任务"""
    if not data["tasks"]:
        print("📭 还没有任务")
        return

    tasks = data["tasks"]

    # 第2步：按优先级排序（调用上面的函数）
    sorted_task = sort_by_priority(tasks)

    # 第3步：显示排序后的任务
    print("\n📋 所有任务（按优先级排序）")

    # 打印表头
    print(f"{'ID':<4} {'状态':<2} {'标题':<20} {'优先级':<4} {'截止日期':<12} "
          f"{'分类':<6}")
    print("-" * 20)

    for task in sorted_task:
        status = "✅" if task["completed"] else "⬜"
        print(
            f"{task['id']:<4} {status:<2} {task['title']:<20} {task['priority']:<4} {task['deadline']:<12} "
            f"{task['category']:<6}")

    print("=" * 60)
    print(f"总共：{len(tasks)}个任务")


def show_statistics(data):
    """显示任务统计信息"""
    tasks_list = data["tasks"]

    # 第2步：初始化计数器
    total_count = len(tasks_list)
    completed = 0
    high = 0
    medium = 0
    low = 0

    for task in tasks_list:
        if task["completed"]:
            completed += 1

        # 可以改成 if-elif 结构
        if task["priority"] == "高":
            high += 1
        elif task["priority"] == "中":
            medium += 1
        else:
            low += 1

    # 计算未完成和完成率
    pending = total_count - completed
    complete_rate = (completed / total_count * 100) if \
        total_count > 0 else 0

    print("=" * 30)
    print("📊 任务统计")
    print("=" * 30)
    print(f"总任务数：{total_count}")
    print(f"已完成：{completed}")
    print(f"未完成：{pending}")
    print(f"完成率：{complete_rate:.1f}%")
    print("-" * 30)
    print(f"高优先级：{high}")
    print(f"中优先级：{medium}")
    print(f"低优先级：{low}")
    print("=" * 30)


def complete_task(data):
    """标记任务为已完成"""

    # 第1步：先显示所有任务，让用户看到有哪些ID
    show_all_tasks(data)

    # 第2步：如果没有任务，直接返回
    if not data["tasks"]:
        print("📭 还没有任务")
        return data

    # 第3步：让用户输入要完成的ID
    # finish_id = int(input("请输入要完成的ID："))
    try:
        finish_id = int(input("请输入要完成的ID："))
    except ValueError:
        print("❌ 请输入数字")
        return data

    # 第4步：遍历查找匹配的ID
    flag = False
    for task in data["tasks"]:
        if task["id"] == finish_id:
            task["completed"] = True
            print(f"✅ 任务 {finish_id} 已完成")
            flag = True
            break

    if not flag:
        print("没有找到匹配的信息")

    # 第7步：返回 data
    return data


def delete_task(data):
    """按ID删除任务"""

    # 第1步：先显示所有任务，让用户看到有哪些ID
    show_all_tasks(data)

    # 第2步：如果没有任务，直接返回
    if not data["tasks"]:
        print("📭 还没有任务")
        return data

    try:
        delete_id = int(input("请输入要删除的ID："))
    except ValueError:
        print("❌ 请输入数字")
        return data

    for i, task in enumerate(data["tasks"]):
        if task["id"] == delete_id:
            deleted = data["tasks"].pop(i)
            print(f"✅ 已删除：{deleted['title']}")
            return data

    print(f"❌ 任务 {delete_id} 不存在")


# ===== 主菜单 =====

def main():
    """主程序"""
    # 加载数据
    data = load_data()

    while True:
        print("\n" + "=" * 40)
        print("📋 待办清单管理系统")
        print("=" * 40)
        print("1. 添加任务")
        print("2. 查看所有任务")
        print("3. 查看今日任务")
        print("4. 完成任务")
        print("5. 删除任务")
        print("6. 查看统计")
        print("7. 退出")
        print("=" * 40)

        choice = input("请选择操作：")

        if choice == "1":
            data = add_task(data)
        elif choice == "2":
            show_all_tasks(data)
        elif choice == "3":
            show_today_tasks(data)
        elif choice == "4":
            data = complete_task(data)
        elif choice == "5":
            data = delete_task(data)
        elif choice == "6":
            show_statistics(data)
        elif choice == "7":
            save_data(data)
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    main()

