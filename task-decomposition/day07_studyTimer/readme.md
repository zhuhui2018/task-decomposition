# 📝 项目笔记：学习计时器

## 2024-03-07
### 遇到的问题
- `show_today_progress` 里 gap 计算位置不对
    - 原因：放在判断 target 外面，target 为 None 时报错
    - 解决：移到 if hasattr 里面

### 学到的知识点
- `hasattr(obj, 'attr')` 判断对象是否有属性
- 函数返回字典比返回多个值更清晰

  📝 remove vs pop 的区别
  方法	      作用	                例子
  remove(x)	  删除值为 x 的第一个元素	records.remove(record_obj)
  pop(i)	  删除索引为 i 的元素	    records.pop(0) 删除第一个
  你要的是「按索引删除」，所以用 pop(i)。

⚠️ 重要提醒
remove() 的两个坑：
1，只删第一个（如果有重复，后面的不删）
2，元素不存在会报错（要先判断 if x in list:）

### 明天要做的
- [ ] 导出 CSV 功能
- [ ] 复习装饰器

### 待优化
- [ ] `get_today_progress` 可以加缓存
- [ ] 显示格式统一用 emoji

思考：
1，为什么要有休息类和学习类，父类中为什么要有display方法，
父类中没有这个方法会怎么样，如果父类只有属性没有方法可以嘛
2，studyTracker中的total_records = 0为什么是存的类变量而不是实例变量
那什么时候用类变量什么时候用实例变量呢
3，self.records = [] 实例变量中怎么想到要用列表存储的















