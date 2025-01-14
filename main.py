from nicegui import ui


def greet():
    name = name_input.value
    greeting_label.text = f'Hello, {name}!'

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

# 创建一个简单的文本输入框和按钮
ui.label('Enter your name:')
name_input = ui.input().style('width: 200px;')

greeting_label = ui.label('')

# 创建一个按钮，点击时会显示问候
ui.button('Greet me!', on_click=greet)

# 启动应用
ui.run(host="0.0.0.0", port=5000)
