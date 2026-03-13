# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

import json
from datetime import datetime
import csv  # 记得在文件开头导入


class Record:
    def __init__(self, date, duration, note):
        self.date = date
        self.duration = duration
        self.note = note

    def display(self):
        # 把存的数据拿出来用
        return f"{self.date} {self.duration}分钟 " \
               f"{self.note}"


class StudyRecord(Record):
    def __init__(self, date, duration, subject, note):
        super().__init__(date, duration, note)
        self.subject = subject

    def display(self):
        # 把存的数据拿出来用
        return f"{self.date} {self.subject} {self.duration}分钟 " \
               f"{self.note}"


class BreakRecord(Record):
    def __init__(self, date, duration, note):
        super().__init__(date, duration, note)
        self.type = "休息"

    def display(self):
        # 把存的数据拿出来用
        return f"{self.date} 休息 {self.duration}分钟 " \
               f"{self.note}"


class StudyTracker:
    # 1. 类变量：total_records
    total_records = 0

    def __init__(self):
        self.records = []  # 存所有记录（学习+休息）

    def save_to_file(self, filename="study_data.json"):
        """保存数据到文件"""
        data = []
        for record in self.records:
            if isinstance(record, StudyRecord):
                data.append({
                    "type": "study",
                    "date": record.date,
                    "duration": record.duration,
                    "subject": record.subject,
                    "note": record.note
                })
            else:  # BreakRecord
                data.append({
                    "type": "break",
                    "date": record.date,
                    "duration": record.duration,
                    "note": record.note
                })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ 数据已保存到 {filename}")

    def load_from_file(self, filename="study_data.json"):
        """从文件加载数据"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.records = []
            for item in data:
                if item["type"] == "study":
                    record = StudyRecord(
                        item["date"],
                        item["duration"],
                        item["subject"],
                        item["note"]
                    )
                else:
                    record = BreakRecord(
                        item["date"],
                        item["duration"],
                        item["note"]
                    )
                self.records.append(record)

            print(f"✅ 已从 {filename} 加载 {len(self.records)} 条记录")
        except FileNotFoundError:
            print("📭 没有找到历史数据，开始新的记录")
        except Exception as e:
            print(f"❌ 加载失败：{e}")

    def add_study(self, date, duration, subject, note):
        """添加学习记录"""
        # 创建 StudyRecord 对象
        # 添加到 self.records 列表
        study = StudyRecord(date, duration, subject, note)
        self.records.append(study)
        StudyTracker.total_records += 1

    def add_break(self, date, duration, note):
        """添加休息记录"""
        # 创建 BreakRecord 对象
        # 添加到 self.records 列表
        break_sec = BreakRecord(date, duration, note)
        self.records.append(break_sec)
        StudyTracker.total_records += 1

    def show_all(self):
        """显示所有记录"""
        for record in self.records:
            print(record.display())

    def get_stats(self):
        """添加统计功能"""

        study_time = 0
        break_time = 0
        for record in self.records:
            if isinstance(record, StudyRecord):
                study_time += record.duration
            elif isinstance(record, BreakRecord):
                break_time += record.duration

        return {
            "总学习时间": study_time,
            "总休息时间": break_time,
            "记录总数": len(self.records),
            "全局记录总数": StudyTracker.total_records  # 类变量
        }

    def get_by_date(self, date):
        """添加按日期筛选"""
        # 我想的逻辑是要区分是学习类还是休息类，分别过滤添加，
        # 其实这里就是要把学习和休息当成一个整体，只考虑日期
        result = []
        for record in self.records:
            if record.date == date:
                result.append(record)
        return result

    def total_study_time(self):
        """计算总学习时间（只统计学习记录）"""
        total = 0
        for record in self.records:
            if isinstance(record, StudyRecord):
                total += record.duration
        return total

    def get_subject_stats(self):
        """统计每个科目的学习总时长"""
        subject_time = {}

        for record in self.records:
            if isinstance(record, StudyRecord):
                # subject_time[record.subject] = record.duration 这里逻辑有点问题，
                # 结果会导致同一条记录被执行两次
                if record.subject not in subject_time:
                    subject_time[record.subject] = record.duration
                else:
                    subject_time[record.subject] += record.duration

        return subject_time

    def set_daily_target(self, target_minutes):
        """设置每日学习目标"""
        self.daily_target = target_minutes

    def check_daily_progress(self, date):
        """检查某天是否达成目标"""
        # 这个方法逻辑要是首先能想到把某天的记录全部获取到，
        # 再去找学习类，时间累加就很清晰，但是如果首先想到的是先获取学习类，
        # 再去对比日期，要是日期一致，就去累加学习时间，就会稍微复杂一点
        if not hasattr(self, 'daily_target'):
            return "请先设置每日目标", 0, None

        total_study_time = 0
        total_record = self.get_by_date(date)

        # 2. 累加当天的学习时长（只统计 StudyRecord）
        for study_record in total_record:
            if isinstance(study_record, StudyRecord):
                total_study_time += study_record.duration

        if total_study_time >= self.daily_target:  # >= 更合理
            return True, total_study_time, self.daily_target
        else:
            return False, total_study_time, self.daily_target

    def show_with_index(self):
        """显示所有记录（带编号）"""

        # 1. 判断是否有记录
        if not self.records:
            print("📭 目前还没有任何记录")
            return None

        for i, record in enumerate(self.records):
            print(f"{i}, {record.display()}")

    def delete_by_index(self, index):
        """按索引删除记录"""
        if index < 0 or index >= len(self.records):
            print(f"❌ 索引 {index} 无效")
            return None

        deleted = self.records.pop(index)
        print(f"✅ 已删除：{deleted.display()}")

        return deleted

    def delete_interactive(self):
        """交互式删除记录"""

        self.show_with_index()
        if not self.records:
            return

        try:
            idx = int(input("请输入要删除的索引："))
        except Exception as e:
            print(e, "请输入数字")
            return

        self.delete_by_index(idx)

    def update_by_index(self, index, field, new_value):
        """按索引修改记录的某个字段"""

        # 1. 判断索引是否有效
        if index < 0 or index >= len(self.records):
            print("❌ 索引无效")
            return None

        # 2. 根据 field 修改对应的属性
        # field 可以是 "date"、"duration"、"subject"、"note"
        # 刚开始自己没有理解filed的意思，其实就是传入要修改的字段
        record = self.records[index]
        if field == "date":
            record.date = new_value
        elif field == "duration":
            record.duration = new_value
        elif field == "subject":
            if isinstance(record, StudyRecord):
                record.subject = new_value
            else:
                print("❌ 休息记录没有科目字段")
                return None
        elif field == "note":
            record.note = new_value
        else:
            print("❌ 无效的字段名")
            return None
        print(f"✅ 修改成功：{record.display()}")
        return record

    def update_interactive(self):
        """交互式修改记录"""
        self.show_with_index()

        if not self.records:
            return

        try:
            idx = int(input("请输入要修改的索引："))
        except Exception as e:
            print(e, "请输入数字")
            return

        record = self.records[idx]

        if isinstance(record, StudyRecord):
            print("可修改的字段：0.日期 1.时长 2.科目 3.备注")
            field_map = {0: "date", 1: "duration", 2: "subject", 3: "note"}
            max_choice = 3
        else:
            print("可修改的字段：0.日期 1.时长 2.备注")
            field_map = {0: "date", 1: "duration", 2: "note"}
            max_choice = 2

        try:
            field_choice = int(input("请选择要修改的字段编号："))
            if field_choice < 0 or field_choice > max_choice:
                print(f"❌ 字段编号必须在 0-{max_choice} 之间")
                return
            field = field_map[field_choice]
        except ValueError:
            print("❌ 请输入数字")
            return

        new_value = input("请输入要修改的新值：")

        if field == "duration":
            try:
                new_value = int(new_value)
            except ValueError:
                print("❌ 时长必须为数字")
                return

        self.update_by_index(idx, field, new_value)

    def get_stats_by_period(self, start_date, end_date):
        """统计某段时间内的学习情况"""

        # 1. 初始化统计变量（学习总时长、休息总时长）
        total_result = {"study_time": 0,
                        "break_time": 0}

        # 2. 遍历所有记录
        for record in self.records:
            if start_date <= record.date <= end_date:
                if isinstance(record, StudyRecord):
                    total_result["study_time"] += record.duration
                else:
                    total_result["break_time"] += record.duration
        return total_result

    def period_stats_interactive(self):
        """交互式时间段统计"""

        try:
            start = input("请输入开始日期 (YYYY-MM-DD)：")
            end = input("请输入结束日期 (YYYY-MM-DD)：")

            if len(start) != 10 or len(end) != 10:
                print("❌ 日期格式应为 YYYY-MM-DD")
                return

            stats = self.get_stats_by_period(start, end)
            days = self._count_days_in_period(start, end)

            print(f"\n📊 {start} 至 {end} 统计")
            print(f"总学习时间：{stats['study_time']} 分钟")
            print(f"总休息时间：{stats['break_time']} 分钟")

            if days > 0:
                avg = stats['study_time'] / days
                print(f"平均每天学习：{avg:.1f} 分钟")

                # 和目标对比
                if hasattr(self, 'daily_target'):
                    if avg >= self.daily_target:
                        print(f"🎉 平均学习时间达到目标（{self.daily_target}分钟/天）！")
                    else:
                        diff = self.daily_target - avg
                        print(f"📉 比目标少 {diff:.1f} 分钟/天")

        except Exception as e:
            print(f"❌ 输入错误：{e}")

    def _count_days_in_period(self, start_date, end_date):
        """计算时间段内的天数"""
        from datetime import datetime
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            return (end - start).days + 1
        except:
            return 0

    def get_week_stats(self):
        """按周统计学习时间"""
        week_stats = {}  # 键：(year, week)，值：总学习时间

        for record in self.records:
            if isinstance(record, StudyRecord):
                # 获取日期对象
                date = datetime.strptime(record.date, "%Y-%m-%d")
                # 获取年份和周数
                year, week, _ = date.isocalendar()

                key = (year, week)
                week_stats[key] = week_stats.get(key, 0) + record.duration

        return week_stats

    def _get_week_range(self, year, week):
        """获取某年某周的起止日期（返回月-日）"""
        # 找到该周的第一天（周一）
        first_day = datetime.strptime(f"{year}-{week}-1", "%Y-%W-%w")
        last_day = first_day.replace(day=first_day.day + 6)

        return first_day.strftime("%m-%d"), last_day.strftime("%m-%d")

    def show_week_stats(self):
        """显示按周统计"""
        stats = self.get_week_stats()

        if not stats:
            print("📭 没有学习记录")
            return

        print("\n📊 按周统计")
        print("=" * 40)

        # 按键排序（先年，后周）
        for (year, week) in sorted(stats.keys()):
            start, end = self._get_week_range(year, week)
            total = stats[(year, week)]
            print(f"{year}年第{week:02d}周 ({start}~{end})：{total} 分钟")

        print("=" * 40)

    def filter_by_subject(self, subject):
        """返回该科目的所有学习记录"""
        study_result = []
        for record in self.records:
            if isinstance(record, StudyRecord):
                if record.subject.lower() == subject.lower():
                    study_result.append(record)
        return study_result

    def filter_subject_interactive(self):
        """交互式按科目筛选"""
        subject = input("请输入要查看的科目：")
        study_result = self.filter_by_subject(subject)
        if not study_result:
            print(f"📭 没有找到 [{subject}] 科目的记录")
            return
        for study in study_result:
            print(f"{study.date} {study.subject} {study.duration}")
        print(f"共找到 {len(study_result)} 条记录")

    def sort_by_date(self, reverse=False):
        """按日期排序（默认正序）"""
        # 用 sorted 排序
        sorted_date = sorted(self.records, key=lambda record: record.date, reverse=reverse)
        return sorted_date

    def show_sorted_by_date(self):
        """交互式按日期排序显示"""

        choice = input("请选择排序方式（1.正序 2.倒序）：")

        # 2. 根据选择设置 reverse
        if choice == "2":
            reverse = True
        else:
            reverse = False

        # 2. 调用 sort_by_date
        sorted_date = self.sort_by_date(reverse)

        # 4. 显示结果
        print(f"\n📋 所有记录（按日期{'倒序' if reverse else '正序'}）")
        for data in sorted_date:
            print(data.display())

    def get_today_progress(self):
        """获取今日学习进度"""

        today_study = 0

        # 1. 获取今天的日期
        today = datetime.now().strftime("%Y-%m-%d")  # 这里有坑，
        # 比较日期的话要转换成字符串去比较，datetime.now()是对象，没法直接比较，
        # 所以有日期的时候还是得想想是要做什么，

        # 2. 累加今天的学习时长
        for record in self.records:
            if isinstance(record, StudyRecord):
                if record.date == today:
                    today_study += record.duration

        # 3. 获取每日目标（如果有）
        if hasattr(self, 'daily_target'):
            target = self.daily_target
        else:
            target = None

        # return target, today_study  #我没有考虑到这个返回值方不方便下个函数调用
        return {
            "date": today,
            "study_time": today_study,
            "target": target
        }

    def show_today_progress(self):
        """显示今日进度"""
        # 这个方法我写的有问题的地方 把gap = study - target 放在了外面，
        # 如果目标为空，岂不是gap就有问题了

        # 1. 调用 get_today_progress 获取数据
        today_study = self.get_today_progress()

        # 2. 显示今日日期
        print(f"📅 今日日期：{today_study['date']}")

        # 3. 显示学习时长
        print(f"📚 今日学习：{today_study['study_time']}分钟")
        if hasattr(self, 'daily_target'):
            target = today_study['target']
            study = today_study['study_time']
            gap = study - target

            print(f"🎯 今日目标：{target} 分钟")
            if gap > 0:
                print(f"今日目标已经完成，多学习{gap}时间")
            else:
                print(f"今日目标未完成，还差{-gap}时间")
        else:
            print("⚠️ 今日目标未设置")

    def search(self, keyword):
        """按关键词搜索记录"""
        # 这里的逻辑值得好好的多看几遍，为什么我想到的是根据关键词去在学习类和休息类中去匹配，
        # 而更好的是在学习类或者休息类中去匹配关键词
        # 我这个缺点是你怎么知道关键词是科目还是note，而休息类中没有科目，这就会导致很混乱，
        # 但是直接根据大类（学习类或者休息类）中去匹配关键词就没有这个问题，
        # 这就是一个很好的思维训练，可以想想还可以用在哪些地方

        # 1. 创建一个空列表存放结果
        search_result = []

        for record in self.records:
            if isinstance(record, StudyRecord):
                if keyword.lower() in record.subject or keyword in record.note:
                    search_result.append(record)
            elif isinstance(record, BreakRecord):
                if keyword.lower() in record.note:
                    search_result.append(record)
        return search_result

    def search_interactive(self):
        """交互式搜索"""

        # 1. 让用户输入关键词
        keyword = input("请输入要搜索的关键词：")
        # 2. 调用 search
        search_result = self.search(keyword=keyword)
        # 3. 如果没有结果，提示
        if not search_result:
            print("没有找到匹配的记录")

        for result in search_result:
            print(result.display())

    def export_to_csv(self, filename="study_records.csv"):
        """导出记录到 CSV 文件"""

        if not self.records:
            print("📭 没有记录可导出")
            return

        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)

                # 写表头
                writer.writerow(['日期', '类型', '科目', '时长', '备注'])

                # 写数据
                for record in self.records:
                    if isinstance(record, StudyRecord):
                        writer.writerow([
                            record.date,
                            '学习',
                            record.subject,
                            record.duration,
                            record.note
                        ])
                    else:  # BreakRecord
                        writer.writerow([
                            record.date,
                            '休息',
                            '',  # 科目为空
                            record.duration,
                            record.note
                        ])

            print(f"✅ 已导出 {len(self.records)} 条记录到 {filename}")

        except Exception as e:
            print(f"❌ 导出失败：{e}")

    def export_interactive(self):
        """交互式导出 CSV"""

        filename = input("请输入文件名（默认 study_records.csv）：").strip()
        if not filename:
            filename = "study_records.csv"

        # 确保文件名以 .csv 结尾
        if not filename.endswith('.csv'):
            filename += '.csv'

        self.export_to_csv(filename)


# 创建 tracker 对象
tracker = StudyTracker()

# 添加几条不同日期的记录
tracker.add_study("2026-03-09", 120, "Python", "第一天")
tracker.add_study("2026-03-09", 60, "Java", "也是第一天")
tracker.add_break("2026-03-09", 15, "休息一下")

tracker.add_study("2026-03-09", 90, "Python", "第二天")
tracker.add_break("2026-03-09", 10, "喝咖啡")

tracker.add_study("2026-03-09", 180, "JavaScript", "第三天")

# 测试1：获取某一天的所有记录
print("=" * 40)
print("测试 get_by_date('2026-03-09')")
print("=" * 40)
records_01 = tracker.get_by_date("2026-03-09")
for r in records_01:
    print(r.display())
print(f"共 {len(records_01)} 条记录")

# 测试2：获取另一天的记录
print("\n" + "=" * 40)
print("测试 get_by_date('2026-03-10')")
print("=" * 40)
records_02 = tracker.get_by_date("2026-03-10")
for r in records_02:
    print(r.display())
print(f"共 {len(records_02)} 条记录")

# 测试3：获取没有记录的那天
print("\n" + "=" * 40)
print("测试 get_by_date('2026-03-15')（没有记录）")
print("=" * 40)
records_04 = tracker.get_by_date("2026-03-15")
if not records_04:
    print("当天没有记录")
else:
    for r in records_04:
        print(r.display())
print(f"共 {len(records_04)} 条记录")

# 测试4：查看所有记录（确认数据）
print("\n" + "=" * 40)
print("所有记录：")
print("=" * 40)
tracker.show_all()
print(tracker.get_subject_stats())
tracker.set_daily_target(120)
print(tracker.check_daily_progress("2026-03-09"))  # 达标

tracker.delete_by_index(0)  # 删除第一条
tracker.delete_by_index(5)  # 索引无效
tracker.delete_by_index(-1)  # 索引无效
print("删除前：")
tracker.delete_interactive()

print("\n删除后：")
tracker.show_with_index()

# 导出到默认文件
tracker.export_to_csv()

# 指定文件名
tracker.export_to_csv("我的学习记录.csv")

# 交互式
tracker.export_interactive()