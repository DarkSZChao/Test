import asyncio
import os

from nicegui import app, ui, run

# set default saving dir
DEFAULT_SAVING_DIR = os.path.join(os.getcwd(), "downloads")

# expose the background image dir
app.add_static_files("/static", "static")

# set background
ui.add_head_html("""
<style>
    body {
        background-image: url('/static/background.jpg');
        background-size: cover;
        background-position: center;
        margin: 0;
        font-family: Arial, sans-serif;
    }
    .container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
        max-width: 400px;
        margin: auto;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }
    .centered {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>
""")

previous_buffer = ''
radio_method_options = ['Single YouTube URL', 'YouTube Playlist URL']

# define GUI items
with ui.card().style('max-width: 800px;').classes('container'):
    with ui.row().style('width: 100%'):
        ui.label("YouTube MP3 Downloader").classes("text-h4 text-center")

    with ui.row().style('width: 100%'):
        radio_method = ui.radio(radio_method_options, value='Single YouTube URL').props('inline')
        radio_method.disable()
    with ui.row().style('width: 100%'):
        input_url = ui.input(label="Pls enter YouTube URL",
                             placeholder="https://www.youtube.com/watch?v=example").style('width: 100%;')

with ui.card().style('max-width: 800px;').classes('container'):
    with ui.row().style('width: 100%'):
        ui.label('Save MP3 to...').classes("text-h5 text-center")

    with ui.row().style('width: 100%').classes('justify-between'):
        input_dir = ui.input(label='Directory:', placeholder=DEFAULT_SAVING_DIR).style('width: 85%;')
        button_dir = ui.button('Select').style('margin-top: 10px')

    with ui.row().style('width: 100%'):
        label_info = ui.label('Downloader ready...').style('color: green; margin-top: 10px').classes("text-h6 text-center")

    with ui.row().style('width: 100%').classes('justify-end'):
        button_download = ui.button("Download MP3").style('margin-top: 10px')

ui.run(host="0.0.0.0", port=5050)  # reload=False is necessary for pyinstaller
