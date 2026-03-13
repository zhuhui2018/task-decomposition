# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22

# 日志备份

import os
import shutil
from datetime import datetime
import glob


class BackupManager:
    def __init__(self, source_file, backup_dir, count):
        # 把零件存起来
        self.source_file = source_file
        self.backup_dir = backup_dir
        self.count = count

        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)

    def backup(self):
        # 执行备份操作
        backup_path = self._generate_filename()
        shutil.copy2(self.source_file, backup_path)

    def _generate_filename(self):
        # 生成带时间戳的文件名（内部用）
        filename = os.path.basename(self.source_file)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{self.backup_dir}/{name}_{timestamp}{ext}"
        return backup_file

    def _clean_old(self):
        # 清理旧备份（内部用）
        name = os.path.splitext(os.path.basename(self.source_file))[0]
        pattern = f"{self.backup_dir}/{name}_*.py"
        backups = glob.glob(pattern)  # 匹配出所有备份文件
        backups.sort(key=os.path.getmtime, reverse=True)  # 按修改时间排序（最旧的在最前面）
        if len(backups) <= self.count:
            return

        # 删除多余的
        for old_file in backups[self.count:]:
            os.remove(old_file)

    def list_backups(self):
        # 查看操作
        print("1111", f"{self.backup_dir}/{os.path.basename(self.source_file)}")
        pattern = f"{self.backup_dir}/{os.path.basename(self.source_file).replace('.', '_*')}"
        print("pattern", pattern)
        backups = glob.glob(pattern)
        print("backups", backups)
        backups.sort(key=os.path.getmtime, reverse=True)

        if not backups:
            print("📭 没有找到任何备份")
            return

        print(f"\n📋 备份列表（共 {len(backups)} 个）")
        for i, f in enumerate(backups, 1):
            size = os.path.getsize(f) / 1024  # KB
            mtime = datetime.fromtimestamp(os.path.getmtime(f))
            print(f"{i}. {os.path.basename(f)} ({size:.1f} KB) - {mtime}")

    def restore(self, index):
        # 恢复操作
        # 1. 找出所有备份文件

        name = os.path.splitext(os.path.basename(self.source_file))[0]
        pattern = f"{self.backup_dir}/{name}_*.py"
        backups = glob.glob(pattern)
        backups.sort(key=os.path.getmtime, reverse=True)

        # 2. 如果没有备份，直接返回
        if not backups:
            print("📭 没有找到任何备份，无法恢复")
            return False

        # 3. 确定要恢复哪个备份
        if 0 <= index < len(backups):
            backup_file = backups[index]
        else:
            print(f"❌ 索引无效，有效范围 0-{len(backups)-1}")
            return False

        # 4. 显示备份信息
        filename = os.path.basename(backup_file)
        size = os.path.getsize(backup_file) / 1024
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_file))
        print(f"📋 备份文件：{filename}")
        print(f"📋 文件大小：{size:.1f} KB")
        print(f"📋 备份时间：{mtime}")

        # 5. 确认恢复（可选）
        confirm = input("⚠️ 恢复会覆盖当前数据，确定吗？(y/n)：")
        if confirm.lower() != 'y':
            print("❌ 已取消恢复")
            return False

        # 6. 执行恢复（复制备份文件回原位置）
        try:
            shutil.copy2(backup_file, self.source_file)
            print(f"✅ 恢复成功！当前数据已替换为备份版本")
            return True
        except Exception as e:
            print(f"❌ 恢复失败：{e}")
            return False


source_file = "log_backup.py"
backup_dir = "log"
count = 10
backup_m = BackupManager(source_file, backup_dir, count)
backup_m.backup()  # 执行一次备份
backup_m.list_backups()
backup_m.restore(0)