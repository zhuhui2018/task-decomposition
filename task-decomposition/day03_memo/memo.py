# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22
import json
import time
from datetime import datetime


# ===== 文件操作 =====

def load_data():
    """从文件加载数据"""
    try:
        with open("memo.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"memos": []}


def save_data(data):
    """保存数据到文件"""
    with open("memo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ===== 添加备忘录 =====

def add_memo(data):
    """添加新备忘录"""
    print("\n📝 添加新备忘录")

    # 1. 生成ID（用时间戳）
    # 请填写：用time.time()获取当前时间戳，转成字符串
    current_id = str(int(time.time()))

    # 2. 输入标题
    # 请填写：用input获取标题
    # 如果用户直接回车，标题设为"无标题"
    title = input("请输入标题：")
    if not title:
        title = "无标题"

    # 3. 输入内容
    # 请填写：用input获取内容
    content = input("请输入内容：")

    # 4. 获取当前日期
    # 请填写：用datetime.now()获取当前日期，格式化成 YYYY-MM-DD
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 5. 输入标签
    print("可选标签：学习、工作、生活、其他")
    # 请填写：用input获取标签
    # 如果用户输入的不在可选标签里，默认设为"其他"
    tag = input("请选择标签：")
    if tag not in ["学习", "工作", "生活", "其他"]:
        tag = "其他"

    # 6. 输入备注（可选）
    # 请填写：用input获取备注
    # 如果用户直接回车，备注设为"无"
    remark = input("备注（可选）：")
    if not remark:
        remark = "无"

    # 7. 输入优先级
    print("优先级：1.高 2.中 3.低")
    # 请填写：用input获取选择
    # 如果输入"1"就转成"高"，"2"转"中"，"3"转"低"
    # 如果输入其他，默认"中"
    priority = input("请输入优先级：")
    if priority == "1":
        priority = "高"
    elif priority == "2":
        priority = "中"
    elif priority == "3":
        priority = "低"
    else:
        priority = "中"

    # 8. 状态默认"未完成"
    status = "未完成"

    # 9. 创建新备忘录（用你设计的数据结构）
    # 请填写：创建一个字典，包含所有字段
    # id, title, content, date, tag, remark, priority, status
    memo = {
        "id": current_id,
        "title": title,
        "content": content,
        "date": current_date,
        "tag": tag,
        "remark": remark,
        "priority": priority,
        "status": status
    }

    # 10. 添加到data["memos"]列表
    # 请填写：用append方法添加
    data["memos"].append(memo)

    print(f"✅ 添加成功")
    return data


# ===== 查看所有备忘录 =====
def show_all_memos(data):
    """查看所有备忘录"""
    # 1. 判断是否有备忘录
    if not data["memos"]:
        print("📭 还没有备忘录")
        return

    print("\n📋 所有备忘录")
    print("=" * 70)

    # 可以加个表头，更清晰
    print(f"{'ID':<15} {'日期':<10} {'优先级':<4} {'标签':<6} {'状态':<6} {'标题'}")
    print("-" * 70)

    for memo in data["memos"]:
        print(
            f"{memo['id']:<15} {memo['date']} {memo['priority']:<4} {memo['tag']:<6} {memo['status']:<6} {memo['title']}")

    print("=" * 70)
    print(f"总共：{len(data['memos'])}条备忘录")


# ===== 查看单个备忘录 =====
def show_memo_detail(data):
    """查看单个备忘录详情"""

    # 1. 先显示所有备忘录
    show_all_memos(data)

    # 2. 如果没有备忘录，返回
    if not data["memos"]:
        return

    # 3. 让用户输入要查看的ID或标题关键词
    search = input("请输入要查看的ID或者标题关键词：")

    # 4. 查找匹配的备忘录
    found = []
    for memo in data["memos"]:
        if search == memo["id"] or search in memo["title"]:
            found.append(memo)

    # 5. 如果没有找到
    if not found:
        print("❌ 没有找到匹配的备忘录")
        return

    # 6. 显示找到的结果
    print(f"\n找到 {len(found)} 条匹配结果：")
    for i, memo in enumerate(found, 1):
        print(f"\n--- 结果{i} ---")
        print(f"ID：{memo['id']}")
        print(f"标题：{memo['title']}")
        print(f"内容：{memo['content']}")
        print(f"日期：{memo['date']}")
        print(f"标签：{memo['tag']}")
        print(f"备注：{memo['remark']}")
        print(f"优先级：{memo['priority']}")
        print(f"状态：{memo['status']}")


def delete_memo(data):
    """删除备忘录"""
    # 1. 先显示所有备忘录（调用哪个函数？）
    show_all_memos(data)

    # 2. 如果没有备忘录，直接返回 data
    if not data["memos"]:
        return data

    # 3. 让用户输入要删除的ID
    # 你的代码：用input获取要删除的ID，存入变量 memo_id
    memo_id = input("请输入要删除的ID：")

    for i, memo in enumerate(data["memos"]):
        if memo["id"] == memo_id:
            deleted = data["memos"].pop(i)
            print(f"✅ 已删除：{deleted['title']}")
            return data

    print(f"❌ 任务 {memo_id} 不存在")
    return data


def main():
    """主程序"""
    # 1. 加载数据（已写好）
    data = load_data()

    while True:
        print("\n" + "=" * 30)
        print("📒 备忘录")
        print("=" * 30)
        print("1. 添加备忘录")
        print("2. 查看所有")
        print("3. 查看详情")
        print("4. 删除备忘录")
        print("5. 退出")
        print("=" * 30)

        choice = input("请选择：")

        if choice == "1":
            # 调用添加函数
            data = add_memo(data)
        elif choice == "2":
            # 调用查看所有函数
            show_all_memos(data)
        elif choice == "3":
            # 调用查看详情函数
            show_memo_detail(data)
        elif choice == "4":
            # 调用删除函数
            data = delete_memo(data)
        elif choice == "5":
            # 保存数据
            save_data(data)
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择")


if __name__ == "__main__":
    # 直接运行主程序
    main()
