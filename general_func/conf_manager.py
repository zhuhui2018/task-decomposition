# -*-coding:UTF-8 -*-
# author: 阿黄  time:2019/10/22
import json
import os


class ConfigManager:
    def __init__(self, filename, config_dir="config",
                 default_config=None):
        # 初始化：存文件名、默认配置
        self.filename = filename
        self.config_dir = config_dir
        self.default_config = default_config or {}
        self.full_path = os.path.join(self.config_dir, self.filename)

        # 确保目录和文件存在
        self._ensure_file()

        # 加载配置到 self.config
        self.config = self.load()

    def _ensure_file(self):
        # 确保配置文件存在，不存在则创建
        # os.makedirs() 是创建目录的，我创建成了文件，所以会报错，显示文件不存在
        os.makedirs(self.config_dir, exist_ok=True)

        if not os.path.exists(self.full_path):
            with open(self.full_path, 'w', encoding='utf-8') as f:
                json.dump(self.default_config, f, ensure_ascii=False,
                          indent=4)

    def get(self, key, default=None):
        # 获取配置项

        keys = key.split(".")
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key, value):
        # 设置配置项

        target = self.config
        keys = key.split(".")
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]

        target[keys[-1]] = value
        self.save()

    def save(self):
        # 保存到文件
        try:
            with open(self.full_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False,
                          indent=4)
            return True
        except Exception as e:
            print(f"❌ 保存失败：{e}")
            return False

    def load(self):
        # 从文件加载
        try:
            with open(self.full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 文件不存在，返回默认配置
            return self.default_config.copy()
        except json.JSONDecodeError:
            # 文件损坏，返回默认配置
            print(f"⚠️ 配置文件 {self.filename} 损坏，使用默认配置")
            return self.default_config.copy()


# 默认配置
default = {
    "database": {
        "host": "localhost",
        "port": 3306
    },
    "debug": False
}

# 创建配置管理器
config = ConfigManager("app_config.json", default_config=default)

# 1. 获取配置（第一次）
print("="*40)
print("第一次获取配置：")
host = config.get("database.host")
port = config.get("database.port", 3306)
debug = config.get("debug", False)

print(f"database.host = {host}")
print(f"database.port = {port}")
print(f"debug = {debug}")

# 2. 修改配置
print("\n" + "="*40)
print("修改配置：")
config.set("database.host", "192.168.1.100")
config.set("debug", True)
print("✅ 修改完成")

# 3. 再次获取配置（验证是否修改成功）
print("\n" + "="*40)
print("修改后再次获取：")
host = config.get("database.host")
port = config.get("database.port", 3306)
debug = config.get("debug", False)

print(f"database.host = {host}")
print(f"database.port = {port}")
print(f"debug = {debug}")

# 4. 查看文件内容
print("\n" + "="*40)
print("查看文件内容：")
with open("config/app_config.json", "r") as f:
    print(f.read())
