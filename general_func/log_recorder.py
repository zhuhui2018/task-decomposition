# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22
import glob
import os
from datetime import datetime


class Logger:
    def __init__(self, name, log_dir="logs", keep_days=7, min_level="INFO",
                 time_format="%Y-%m-%d %H:%M:%S"):
        """
        :param name: 日志文件名前缀
        :param log_dir: 日志存放目录
        :param keep_days: 保留日志天数
        :param min_level: 最低日志级别 (DEBUG, INFO, WARNING, ERROR)
        :param time_format: 时间格式
        """
        # 初始化：创建目录、设置保留天数
        self.log_dir = log_dir
        self.keep_days = keep_days
        self.name = name
        self.last_clean_date = None  # 日志最后清理日期
        self.min_level = min_level
        self.time_format = time_format

        # 级别优先级
        self.level_order = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

    def _need_clean(self):
        """判断今天是否需要清理"""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.last_clean_date != today:
            self.last_clean_date = today
            return True
        return False

    def _should_log(self, level):
        """判断该级别是否应该记录"""
        return self.level_order[level] >= self.level_order[self.min_level]

    def _get_log_file(self):
        # 根据当天日期生成日志文件名
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.name}_{today}.log"
        base_path = os.path.join(self.log_dir, filename)

        if os.path.exists(base_path) and os.path.getsize(base_path) > 10 * 1024 * 1024:
            i = 1
            while True:
                new_filename = f"{self.name}_{today}_{i}.log"
                new_path = os.path.join(self.log_dir, new_filename)
                if os.path.exists(new_path):
                    i += 1
                else:
                    return new_path

        return base_path

    def log(self, level, message):
        # 写入日志：时间 + 级别 + 消息
        if not self._should_log(level):
            return

        now = datetime.now().strftime(self.time_format)
        log_line = f"[{now}] [{level}] {message}\n"

        log_file = self._get_log_file()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line)

        if level == "ERROR":
            error_file = os.path.join(self.log_dir, "error_log")
            with open(error_file, "a", encoding="utf-8") as f:
                f.write(log_line)

        # 每天清理一次旧日志
        clean_log = self._need_clean()
        if clean_log:
            self._clean_old_logs()

    def debug(self, message):
        """记录 DEBUG 级别日志"""
        print(f"[DEBUG] {message}")
        self.log("DEBUG", message)

    def info(self, message):
        """记录 INFO 级别日志（同时打印到控制台）"""
        print(f"[INFO] {message}")  # 调试时能实时看到
        self.log("INFO", message)

    def warning(self, message):
        print(f"[WARNING] {message}")
        self.log("WARNING", message)

    def error(self, message):
        print(f"[ERROR] {message}")
        self.log("ERROR", message)

    def get_log_files(self):
        """获取所有日志文件"""
        pattern = os.path.join(self.log_dir, f"{self.name}_*.log")
        files = glob.glob(pattern)
        return files

    def _clean_old_logs(self):
        # 清理超过 keep_days 的旧日志
        log_list = self.get_log_files()
        log_list.sort(key=os.path.getmtime, reverse=True)
        for log_file in log_list[self.keep_days:]:
            os.remove(log_file)
            print(f"🗑️ 删除旧日志：{log_file}")


# 测试代码
if __name__ == "__main__":
    # 创建日志器
    logger = Logger("app", "logs", keep_days=2, min_level="INFO")

    # 写不同级别的日志
    logger.debug("这是debug，不会记录")  # 级别太低，不记录
    logger.info("程序启动")
    logger.warning("数据库连接慢")
    logger.error("写入失败")

    print("\n✅ 日志写入完成，请查看 logs 目录")
