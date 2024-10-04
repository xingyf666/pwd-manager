from APP import APP

# 用 tkinter 对象初始化
app = APP('pwd')

# 进行配置
app.tkinit()
app.center()
app.load()

# 开启消息循环
app.loop()

# 保存数据
app.save()