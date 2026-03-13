# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

import json  # 加在文件开头


# ===== 文件操作 =====

def load_data():
    try:
        with open("money.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"records": [], "next_id": 1, "budget": None}  # 加 budget


def save_data(data):
    """保存数据到文件"""
    with open("money.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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

    # 如果是支出，检查预算
    if type_input == "支出":
        check_budget(data)

    return data


def filter_by_month(data, year, month):
    """按年月筛选记录"""
    # 第1步：创建一个空列表，存放筛选结果
    filter_result = []

    # 第2步：遍历所有记录
    # 如果记录的日期（前7个字符）等于 f"{year}-{month:02d}"
    for record in data["records"]:
        if record["date"][:7] == f"{year}-{int(month):02d}":
            filter_result.append(record)
    return filter_result


def show_monthly_report(data):
    """显示月度报表"""

    # 第1步：让用户输入年份
    year = input("请输入年份（如2024）：")

    # 第2步：让用户输入月份
    month = input("请输入月份（如2）：")

    # 第3步：调用 filter_by_month 获取该月的记录
    month_records = filter_by_month(data, year, month)

    # 第4步：如果没有记录，提示并返回
    if not month_records:
        print("没有此记录")
        return

    # 第5步：计算该月总收入和总支出
    # 初始化 total_income = 0, total_expense = 0
    total_income = 0
    total_expense = 0
    for record in month_records:
        # 判断每条记录的类型，累加金额
        if record["type"] == "收入":
            total_income += record["amount"]
        else:
            total_expense += record["amount"]

    # 第5步：打印报表
    print(f"\n📊 {year}年{int(month):02d}月报表")
    print("=" * 40)
    print(f"总收入：{total_income:.2f}元")
    print(f"总支出：{total_expense:.2f}元")
    print(f"结余：{total_income - total_expense:.2f}元")
    print("=" * 40)

    # 第6步：显示该月的所有记录
    print("\n📋 本月明细：")
    for r in month_records:
        print(f"{r['date']} | {r['category']} | "
              f"{r['type']} | {r['amount']:.2f}元 | {r['note']}")


def show_category_stats(data):
    """显示分类统计"""
    categories = ["餐饮", "购物", "交通", "工资", "其他"]
    cate_income = {cate: 0 for cate in categories}
    cate_expense = {cate: 0 for cate in categories}
    print("cate_income", cate_income, "cate_expense", cate_expense)

    for record in data["records"]:
        """这里思路稍微有点卡壳"""
        if record["type"] == "收入":
            cate_income[record["category"]] += record["amount"]
        elif record["type"] == "支出":
            cate_expense[record["category"]] += record["amount"]

    print("\n📊 分类统计")
    print("=" * 50)
    print(f"{'分类':<6} {'收入(元)':<12} {'支出(元)':<12} {'结余(元)':<12}")
    print("-" * 50)

    for cate in categories:
        income = cate_income[cate]
        expense = cate_expense[cate]
        balance = income - expense
        print(f"{cate:<6} {income:<12.2f} {expense:<12.2f} {balance:<12.2f}")

    print("=" * 50)


def show_top_expense_category(data):
    """显示支出最高的分类"""

    categories = ["餐饮", "购物", "交通", "工资", "其他"]
    cate_expense = {cate: 0 for cate in categories}
    total_expense = 0  # 总支出一并统计

    # 2. 遍历统计支出
    for record in data["records"]:
        if record["type"] == "支出":
            cate_expense[record["category"]] += record["amount"]
            total_expense += record["amount"]

    # 3. 找出最高支出的分类
    # max_expense = 0
    # max_category = ""
    # for cate, expense in cate_expense.items():
    #     if expense > max_expense:
    #         max_expense = expense
    #         max_category = cate

    # 3. 找出最高和第二高的支出（这个逻辑有点意思，值得反复琢磨）
    max_expense = 0
    second_expense = 0
    max_category = []  # 存最高分类，为什么要用列表，因为有可能有多个分类
    second_category = []  # 存第二高分类

    for cate, expense in cate_expense.items():
        if expense > max_expense:
            second_expense = max_expense
            second_category = max_category.copy()  # 当开销大于最大值时，那最大值就变成了第二大值，之所有会用到copy，
            # 而不是直接等于最大值分类，是因为最大值是实时变化的，如果直接赋值的话，最大值一变化第二大就跟着改变了

            max_expense = expense
            max_category = [cate]

        elif expense == max_expense:
            # 这个时候是有并列最大值的时候，那把并列最大值分类加到列表中就好了
            second_category.append(cate)

        elif expense > second_expense:
            # 这个时候是大于第二大值小于最大值的时候
            second_expense = expense
            second_category = [cate]

        elif expense == second_expense and expense > 0:
            # 和第二高并列
            second_category.append(cate)

    # 5. 输出结果
    print("\n📊 支出分析")
    print("=" * 50)

    # 显示最高
    if len(max_category) == 1:
        percent = (max_expense / total_expense) * 100
        print(f"🥇 支出最高的分类：{max_category[0]}")
        print(f"   金额：{max_expense:.2f}元，占比：{percent:.1f}%")
    else:
        percent = (max_expense / total_expense) * 100
        print(f"🥇 支出最高的分类（并列）：{', '.join(max_category)}")
        print(f"   金额：{max_expense:.2f}元，占比：{percent:.1f}%")

    # 显示第二高（如果有）
    if second_expense > 0:
        if len(second_category) == 1:
            percent = (second_expense / total_expense) * 100
            print(f"🥈 支出第二高的分类：{second_category[0]}")
            print(f"   金额：{second_expense:.2f}元，占比：{percent:.1f}%")
        else:
            percent = (second_expense / total_expense) * 100
            print(f"🥈 支出第二高的分类（并列）：{', '.join(second_category)}")
            print(f"   金额：{second_expense:.2f}元，占比：{percent:.1f}%")

    print("=" * 50)


def show_expense_chart(data):
    """显示支出比例条形图"""

    # 1. 准备数据
    categories = ["餐饮", "购物", "交通", "工资", "其他"]
    cate_expense = {cat: 0 for cat in categories}
    total_expense = 0

    # 2. 统计支出
    for record in data["records"]:
        if record["type"] == "支出":
            cate_expense[record["category"]] += record["amount"]
            total_expense += record["amount"]

    # 3. 边界情况：没有支出
    if total_expense == 0:
        print("📭 没有支出记录")
        return

    # 4. 把数据转成列表，方便排序
    expense_list = []
    for cate in categories:
        if cate_expense[cate] > 0:
            expense_list.append({
                "category": cate,
                "amount": cate_expense[cate]
            })

    # 5. ⬜ 按金额从大到小排序
    sorted_list = sorted(expense_list, key=lambda x: x["amount"], reverse=True)
    # sorted_list = sorted(expense_list, key=lambda x: x for x in expense_list,
    #                                                           reverse=True)

    # 6. 显示条形图
    print("\n📊 支出比例图（按金额排序）")
    print("=" * 50)

    for item in sorted_list:
        cate = item["category"]
        amount = item["amount"]

        # 计算百分比
        percent = (amount / total_expense) * 100

        # 画条形图（每个█代表2%）
        bar_length = int(percent / 2)
        bar = "█" * bar_length

        # 打印：分类 + 条形图 + 百分比 + 金额
        print(f"{cate}：{bar} {percent:.1f}% ({amount:.2f}元)")

    print("=" * 50)


def set_budget(data):
    """设置本月预算"""
    try:
        budget = float(input("请输入本月预算金额："))
        data["budget"] = budget
        print(f"✅ 本月预算已设置为：{budget:.2f}元")
    except ValueError:
        print("❌ 请输入数字")


def check_budget(data):
    """检查本月预算"""
    if "budget" not in data or data["budget"] is None:
        print("📭 请先设置本月预算")
        return

    from datetime import datetime
    current_month = datetime.now().strftime("%Y-%m")

    total_expense = 0
    for record in data["records"]:
        if record["type"] == "支出" and record["date"][:7] == current_month:
            total_expense += record["amount"]

    budget = data["budget"]
    remaining = budget - total_expense

    print(f"\n💰 本月预算：{budget:.2f}元")
    print(f"当前支出：{total_expense:.2f}元")

    if remaining >= 0:
        print(f"剩余预算：{remaining:.2f}元")
    else:
        print(f"⚠️ 警告：已超支 {-remaining:.2f}元！")


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


def show_records_sorted(data, order="desc"):
    """按金额排序显示所有支出记录"""

    expense_list = []
    for record in data["records"]:
        if record["type"] == "支出":
            expense_list.append(record)  # 存整个记录

    if order == "desc":
        sorted_list = sorted(expense_list, key=lambda x: x["amount"],
                             reverse=True)
    else:
        sorted_list = sorted(expense_list, key=lambda x: x["amount"])

    for r in sorted_list:
        print(f"{r['category']} {r['amount']:.2f}元 {r['date']} {r['note']}")


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


# ===== 主菜单 =====

def main():
    """主程序"""
    # 加载数据
    data = load_data()

    while True:
        print("\n" + "=" * 40)
        print("💰 记账本管理系统")
        print("=" * 40)
        print("1. 添加记录")
        print("2. 查看所有记录")
        print("3. 查看余额统计")
        print("4. 查看月度账单")
        print("5. 显示分类统计")
        print("6. 显示支出最高的分类")
        print("7. 查看支出比例图")
        print("8. 按金额查看支出（从大到小）")
        print("9. 按金额查看支出（从小到大）")
        print("10. 退出")
        print("=" * 40)

        choice = input("请选择操作：")

        if choice == "1":
            data = add_record(data)
        elif choice == "2":
            show_records(data)
        elif choice == "3":
            balance, income, expense = get_balance(data)
            print(f"\n📊 统计信息")
            print("-" * 30)
            print(f"总收入：{income:>10.2f}元")
            print(f"总支出：{expense:>10.2f}元")
            print(f"当前余额：{balance:>10.2f}元")
            print(f"记录总数：{len(data['records'])}条")
        elif choice == "4":
            show_monthly_report(data)
        elif choice == "5":
            show_category_stats(data)
        elif choice == "6":
            show_top_expense_category(data)
        elif choice == "7":
            show_expense_chart(data)
        elif choice == "8":
            show_records_sorted(data, "desc")
        elif choice == "9":
            show_records_sorted(data, "asc")
        elif choice == "10":
            save_data(data)
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    main()
