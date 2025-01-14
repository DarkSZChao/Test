from nicegui import ui


# 创建 NiceGUI 页面
def main():
    # 添加自定义 CSS 以设置背景
    ui.add_head_html('''
    <style>
        body {
            background: url('https://github.com/DarkSZChao/Test/blob/main/background.jpg');
            background-size: cover;
            background-position: center;
            margin: 0;
            padding: 0;
        }
    </style>
    ''')

    # 页面内容
    ui.label("欢迎使用 NiceGUI!").style('font-size: 24px; color: white; margin-bottom: 20px; text-shadow: 2px 2px 4px #000;')

    counter = 0
    label = ui.label(f"当前计数：{counter}").style('font-size: 20px; color: white;')

    def increment():
        nonlocal counter
        counter += 1
        label.set_text(f"当前计数：{counter}")

    ui.button("点击增加计数", on_click=increment).style('margin-top: 20px; background-color: rgba(255, 255, 255, 0.8); border-radius: 8px;')


# 启动 NiceGUI 应用
ui.run(host="0.0.0.0", port=5000)
