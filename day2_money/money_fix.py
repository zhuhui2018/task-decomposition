# -*-coding:UTF-8-*-
# author: 阿黄  time:2019/10/22

def add_record(data):
    """添加新记录"""
    print("\n➕ 添加新记录")

    # 1. 输入类型（收入/支出）
    while True:
        type_input = input("类型（收入/支出）：")
        if type_input in ["收入", "支出"]:
            break
        else:
            print("❌ 只能输入'收入'或'支出'，请重新输入")

    # 2. 输入分类
    print("可选分类：餐饮、购物、交通、工资、其他")
    category = input("分类：")
    if category not in ["餐饮", "购物", "交通", "工资", "其他"]:
        category = "其他"

    # 3. 输入金额
    while True:
        try:
            amount = float(input("金额："))
            if amount <= 0:
                print("❌ 金额必须大于0")
                continue
            break
        except ValueError:
            print("❌ 请输入数字")

    # 4. 输入备注（可选）
    note = input("备注（可选）：")
    if note == "":
        note = "无"

    # 5. 自动生成ID和日期
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    new_record = {
        "id": data["next_id"],
        "date": today,
        "type": type_input,
        "category": category,
        "amount": amount,
        "note": note
    }

    # 7. 添加到records
    data["records"].append(new_record)
    data["next_id"] = data["next_id"] + 1

    print(f"✅ 添加成功：{type_input} {amount:.2f}元")
    return data


def show_records(data):
    """查看所有记录"""
    if not data["records"]:
        print("📭 还没有任何记录")
        return

    print(f"\n{'ID':<4} {'日期':<10} {'类型':<4} {'分类':<6} {'金额':<10} {'备注'}")
    print("-" * 60)

    for r in data["records"]:
        print(f"{r['id']:<4} {r['date']} {r['type']:<4} {r['category']:<6} {r['amount']:<10.2f} {r['note']}")
    print("-" * 60)


def get_balance(data):
    """计算当前余额"""
    total_income = 0
    total_expense = 0

    for r in data["records"]:
        if r["type"] == "收入":
            total_income += r["amount"]
        else:
            total_expense += r["amount"]

    balance = total_income - total_expense
    return balance, total_income, total_expense


if __name__ == "__main__":
    # 初始化数据
    data = {"records": [], "next_id": 1}

    print("💰 记账本测试")
    print("=" * 40)

    # 添加4条测试记录
    for i in range(4):
        print(f"\n--- 第{i+1}条记录 ---")
        data = add_record(data)

    # 显示所有记录
    print("\n📋 所有记录：")
    show_records(data)

    # 显示余额统计
    balance, income, expense = get_balance(data)
    print(f"\n📊 统计信息")
    print("-" * 30)
    print(f"总收入：{income:>10.2f}元")
    print(f"总支出：{expense:>10.2f}元")
    print(f"当前余额：{balance:>10.2f}元")
    print(f"记录总数：{len(data['records'])}条")
    print(f"下一个ID：{data['next_id']}")