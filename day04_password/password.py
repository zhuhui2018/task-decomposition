# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

import time
from datetime import datetime
import json


# ===== 文件操作 =====

def load_data():
    """加载数据"""
    try:
        with open("passwords.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"passwords": []}


def save_data(data):
    """保存数据"""
    with open("passwords.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_password(data):
    """添加密码函数"""
    print("\n📝 添加新密码")

    # 1. 生成ID（用时间戳）
    password_id = str(int(time.time()))

    # 输入网站名称（不能为空）
    while True:
        website = input("请输入网站名称：")
        if not website:
            continue
        break

    # 输入网站地址（可选）
    url = input("请输入网站地址：")
    if not url:
        url = "空"

    # 输入用户名（不能为空）
    while True:
        username = input("请输入用户名：")
        if not username:
            continue
        break

    # 输入密码（不能为空，要考虑用户直接回车的情况）
    password = input("密码：")
    if not password:
        print("密码不能为空，使用默认密码")
        password = "123456"  # 设置默认值

    # 输入备注（可选）
    note = input("请输入备注：")
    if not note:
        note = "空"

    # 输入标签（可选）
    tag = input("请输入标签：")
    if not tag:
        tag = "空"

    # 记录当前时间
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 创建新密码字典
    password = {
        "id": password_id,
        "website": website,
        "url": url,
        "username": username,
        "password": password,
        "note": note,
        "tag": tag,
        "current_time": create_time
    }

    # 添加到 data["passwords"] 列表
    data["passwords"].append(password)

    # 打印成功信息
    print(f"✅ 添加成功")
    return data


def show_all_passwords(data):
    """查看所有密码（密码隐藏显示）"""
    # 1. 判断是否有密码
    # 如果没有，打印提示并返回
    if not data["passwords"]:
        print("📭 还没有密码")
        return

    print("\n📋 所有密码")
    print("=" * 70)

    # 2. 打印表头（ID、网站、用户名、标签）
    # 可以设计成：ID | 网站 | 用户名 | 密码 | 标签
    print(f"{'ID':<15} {'网站':<15} {'用户名':<15} {'密码':<10} {'标签':<10}")
    print("-" * 70)

    # 3. 遍历所有密码
    for pwd in data["passwords"]:
        # 密码隐藏：用 "*" * len(pwd["password"])
        hidden_password = '*' * len(pwd['password'])
        # 打印每一行
        print(
            f"{pwd['id']:<15} {pwd['website']:<15} {pwd['username']:<15} {hidden_password:<10} {pwd['tag']:<10}")

    # 4. 打印总数
    print(f"总共：{len(data['passwords'])}条备忘录")


def show_one_password(data):
    """查看单个密码详情"""

    # 第1步：先调用 show_all_passwords 显示所有密码
    show_all_passwords(data)

    # 第2步：判断如果没有密码，直接返回
    if not data["passwords"]:
        print("📭 还没有密码")
        return

    # 第3步：让用户输入要查看的ID
    passwd_id = input("请输入要查看的ID：")

    # 第4步：遍历查找匹配的ID
    found = None
    for pwd in data["passwords"]:
        if pwd["id"] == passwd_id:
            found = pwd
            break

    # 第5步：如果没找到（found is None），打印提示并返回
    if found is None:
        print("❌ 没有找到匹配的密码")
        return

    # 第6步：显示详细信息
    print(f"\n📌 网站：{found['website']}")
    print(f"🌐 地址：{found['url']}")
    print(f"👤 用户名：{found['username']}")

    # 第7步：询问是否显示密码原文
    # 用 input("是否显示密码原文？(y/n)：") 获取选择
    # 如果输入是 y，显示密码原文
    # 否则显示相同长度的星号
    result = input("是否显示密码原文:[y/n]")
    if result == "y":
        print(f"🔑 密码：{found['password']}")
    else:
        print(f"🔑 密码：{'*' * len(found['password'])}")

    # 第8步：显示备注、标签、创建时间
    print(f"📝 备注：{found['note']}")
    print(f"🏷️ 标签：{found['tag']}")
    print(f"🕐 创建时间：{found['current_time']}")


def delete_password(data):
    """删除密码"""

    # 第1步：先调用 show_all_passwords 显示所有密码
    show_all_passwords(data)

    # 第2步：如果没有密码，返回 data
    if not data["passwords"]:
        print("📭 还没有密码")
        return

    # 第3步：让用户输入要删除的ID
    delete_id = input("请输入要删除的ID：")

    # 第4步：用 enumerate 遍历查找
    for i, pwd in enumerate(data["passwords"]):
        if pwd["id"] == delete_id:
            deleted = data["passwords"].pop(i)
            print(f"✅ 已删除：{deleted['website']}")
            return data

    # 第5步：如果循环结束都没找到，打印提示
    # 返回 data
    print(f"❌ 网站 {delete_id} 不存在")
    return data


def update_password(data):
    """修改密码"""

    # 第1步：先调用 show_all_passwords 显示所有密码
    show_all_passwords(data)

    # 第2步：如果没有密码，返回 data
    if not data["passwords"]:
        print("📭 还没有密码")
        return

    # 第3步：让用户输入要修改的ID
    fix_id = input("请输入要修改的ID：")

    # 第4步：遍历查找，找到后记录索引 i 和字典 pwd
    # 最原始的逻辑有误，就是不管有没有找到，都会执行第5步，然后直接退出去了，应该加一个条件
    # for i, pwd in enumerate(data["passwords"]):
    #     if pwd["id"] == fix_id:
    #         print('pwd["id"]', pwd["id"])
    #         break

    found_index = -1  # 先标记为-1，表示没有找到
    for i, pwd in enumerate(data["passwords"]):
        if pwd["id"] == fix_id:
            found_index = i
            found_pwd = pwd
            break

    # 第5步：如果没找到，打印提示并返回 data
    if found_index == -1:
        print(f"❌ 网站 {fix_id} 不存在")
        return data

    # 第6步：显示当前信息（网站、用户名、备注等）
    # 第6步：显示当前信息
    print(f"\n📌 当前信息：")
    print(f"📝 网站：{found_pwd['website']}")
    print(f"🌐 地址：{found_pwd['url']}")
    print(f"👤 用户名：{found_pwd['username']}")
    print(f"🔑 密码：{'*' * len(found_pwd['password'])}")
    print(f"📝 备注：{found_pwd['note']}")
    print(f"🏷️ 标签：{found_pwd['tag']}")

    # 第7步：让用户选择要修改哪个字段
    print("请选择要修改的字段：")
    print("1. 网站名称")
    print("2. 网站地址")
    print("3. 用户名")
    print("4. 密码")
    print("5. 备注")
    print("6. 标签")
    choice = input("请输入编号：")

    # 第8步：根据选择输入新值
    # 用 if-elif 判断 choice
    # 如果是1：输入新网站名称
    if choice == '1':
        new_value = input("输入新网站名称: ")
        data["passwords"][found_index]["website"] = new_value
    elif choice == '2':
        new_value = input("输入新网址: ")
        data["passwords"][found_index]["url"] = new_value
    elif choice == '3':
        new_value = input("输入新用户名: ")
        data["passwords"][found_index]["username"] = new_value
    elif choice == '4':
        new_value = input("输入新密码: ")
        data["passwords"][found_index]["password"] = new_value
    elif choice == '5':
        new_value = input("输入新内容: ")
        data["passwords"][found_index]["note"] = new_value
    elif choice == '6':
        new_value = input("请输入标签：")
        data["passwords"][found_index]["tag"] = new_value

    # 第10步：打印成功信息
    print("密码信息更新成功")
    return data


def main():
    """主程序"""
    # 加载数据
    data = load_data()

    while True:
        print("\n" + "=" * 30)
        print("🔐 密码管理器")
        print("=" * 30)
        print("1. 添加密码")
        print("2. 查看所有")
        print("3. 查看单个")
        print("4. 修改密码")
        print("5. 删除密码")
        print("6. 退出")
        print("=" * 30)

        choice = input("请选择：")

        if choice == "1":
            data = add_password(data)
        elif choice == "2":
            show_all_passwords(data)
        elif choice == "3":
            show_one_password(data)
        elif choice == "4":
            data = update_password(data)
        elif choice == "5":
            data = delete_password(data)
        elif choice == "6":
            save_data(data)
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择")


if __name__ == "__main__":
    main()
