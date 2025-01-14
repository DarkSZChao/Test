from nicegui import ui


def greet():
    name = name_input.value
    greeting_label.text = f'Hello, {name}!'


# 创建一个简单的文本输入框和按钮
ui.label('Enter your name:')
name_input = ui.input().style('width: 200px;')

greeting_label = ui.label('')

# 创建一个按钮，点击时会显示问候
ui.button('Greet me!', on_click=greet)

# 启动应用
ui.run()
