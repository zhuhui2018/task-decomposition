# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

import json
import os

DATA_FILE = "task.json"


# ========== 文件操作函数 ==========

def load_tasks():
    """程序启动时调用：从文件加载任务"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        print(f"✅ 已加载 {len(tasks)} 个任务")
        return tasks
    except FileNotFoundError:
        print("📭 首次运行，创建新任务列表")
        return []
    except json.JSONDecodeError:
        print("⚠️ 文件损坏，重新创建")
        return []


def save_tasks(tasks):
    """程序关闭前调用：保存任务到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)
    print(f"💾 已保存 {len(tasks)} 个任务")


# ========== 任务操作函数 ==========

def add_task(tasks, next_id, title):
    """添加新任务"""
    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }
    tasks.append(task)
    print(f"✅ 添加任务：{title}")
    return tasks, next_id


def show_tasks(tasks):
    """显示所有任务"""
    if not tasks:
        print("📭 还没有任务")
        return

    print("\n📋 任务清单：")
    for task in tasks:
        status = "✅" if task["completed"] else "⬜"
        print(f"{task['id']}. {status} {task['title']}")


def complete_task(tasks, task_id):
    """完成任务"""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            print(f"✅ 任务 {task_id} 已完成")
            return tasks
    print(f"❌ 任务 {task_id} 不存在")
    return tasks


def delete_task(tasks, task_id):
    """删除任务"""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted = tasks.pop(i)
            print(f"✅ 已删除：{deleted['title']}")
            return tasks
    print(f"❌ 任务 {task_id} 不存在")
    return tasks


# ========== 主程序 ==========

def main():
    """主函数：程序从这里开始"""

    # 1. 启动时加载任务
    tasks = load_tasks()

    # 2. 计算下一个可用ID
    if tasks:
        next_id = max(task["id"] for task in tasks) + 1
    else:
        next_id = 1

    # 3. 简单的命令行界面
    while True:
        print("\n" + "=" * 30)
        print("1. 添加任务")
        print("2. 显示任务")
        print("3. 完成任务")
        print("4. 删除任务")
        print("5. 退出")
        print("=" * 30)

        choice = input("请选择操作：")

        if choice == "1":
            title = input("任务名称： ")
            tasks, next_id = add_task(tasks, next_id, title)

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            task_id = int(input("任务ID"))
            tasks = complete_task(tasks, task_id)

        elif choice == "4":
            task_id = int(input("任务ID："))
            tasks = delete_task(tasks, task_id)

        elif choice == "5":
            # 4. 退出前保存
            save_tasks(tasks)
            print("👋 再见！")
            break

        else:
            print("❌ 无效选择")


# 程序入口
if __name__ == "__main__":
    main()
