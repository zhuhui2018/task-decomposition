# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22
import json


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
                print("data", data)

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

    def set_daily_target(self, target_minutes):
        """设置每日学习目标"""
        self.daily_target = target_minutes

    def check_daily_progress(self, date):
        """检查每日目标是否完成"""
        if not hasattr(self, 'daily_target'):
            return "请先设置每日目标", 0, None

        total_study_time = 0
        for record in self.records:
            if isinstance(record, StudyRecord):
                if record.date == date:
                    total_study_time += record.duration

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

        target = self.records[index]
        self.records.remove(target)
        print(f"✅ 已删除：{target.display()}")  # 只显示被删的，不用遍历全部")

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


studyT = StudyTracker()
studyT.add_study("2026-03-09", 120, "python", "第一天学习")
studyT.add_study("2026-03-10", 60, "python", "第二天学习")
studyT.save_to_file()
# studyT.set_daily_target(130)
# print(studyT.check_daily_progress("2026-03-09"))
studyT.delete_interactive()
