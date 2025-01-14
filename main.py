import asyncio
import os
import tkinter as tk
from tkinter import filedialog

from nicegui import app, ui, run

from check_validation import is_valid_path, is_valid_youtube_url
from downloader import download_youtube_as_mp3

# set default saving dir
DEFAULT_SAVING_DIR = os.path.join(os.getcwd(), "downloads")

# create Tkinter for dir selection
root = tk.Tk()
root.withdraw()  # hide
root.attributes("-topmost", 1)  # top screen the dir selection dialog

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


# disable the items
def disable_GUI_items():
    input_dir.disable()
    input_url.disable()
    button_dir.disable()
    button_download.disable()
    # radio_method.disable()


# enable the items
def enable_GUI_items():
    input_dir.enable()
    input_url.enable()
    button_dir.enable()
    button_download.enable()
    # radio_method.enable()


# use async to keep web GUI alive, put GUi control in this function, use await for backend computation
async def async_callback_button_dir():
    # disable the items
    disable_GUI_items()

    # open dir dialog
    folder_selected = await run.cpu_bound(select_dir)

    # if select any dir
    if folder_selected:
        input_dir.set_value(f'{folder_selected}')
        label_info.style('color: green; margin-top: 10px').set_text(f'The dir [{folder_selected}] is selected.')
        ui.notify(f'The dir [{folder_selected}] is selected.')
    else:
        label_info.style('color: #FF8C00; margin-top: 10px').set_text('No dir is selected, use default.')
        ui.notify('No dir is selected, use default.')

    # enable the items
    enable_GUI_items()


def select_dir():
    return filedialog.askdirectory(title="Select directory")  # select dir


async def async_callback_button_download():
    # disable the items
    disable_GUI_items()

    # check empty URL
    youtube_url = input_url.value
    if not youtube_url:
        label_info.style('color: red; margin-top: 10px').set_text('Enter URL...')
        ui.notify('Enter URL...')
        return
    # check accessible URL
    label_info.style('color: #FF8C00; margin-top: 10px').set_text('Checking URL...')
    ui.notify('Checking URL...')
    res = await run.cpu_bound(is_valid_youtube_url, youtube_url)
    if not res[0]:
        label_info.style('color: red; margin-top: 10px').set_text(res[1])
        ui.notify(res[1])
        return
    else:
        label_info.style('color: green; margin-top: 10px').set_text(res[1])
        ui.notify(res[1])

    await asyncio.sleep(2)

    # get saving dir
    saving_dir = DEFAULT_SAVING_DIR
    if not input_dir.value:
        label_info.style('color: #FF8C00; margin-top: 10px').set_text('No dir selected, saving files to current folder...')
        ui.notify('No dir selected. Saving files to current folder...')
    else:
        res = is_valid_path(input_dir.value)
        if not res[0]:
            input_dir.set_value('')
            label_info.style('color: #FF8C00; margin-top: 10px').set_text(res[1] + ' Saving files to current folder...')
            ui.notify(res[1] + ' Saving files to current folder...')
        else:
            saving_dir = input_dir.value
            label_info.style('color: green; margin-top: 10px').set_text(res[1] + ' Saving files to selected folder...')
            ui.notify(res[1] + ' Saving files to selected folder...')

    await asyncio.sleep(2)

    # download MP3
    label_info.style('color: red; margin-top: 10px').set_text('Downloading MP3...')
    ui.notify('Downloading MP3...')
    try:
        await run.cpu_bound(download_youtube_as_mp3, youtube_url, saving_dir)
        label_info.style('color: green; margin-top: 10px').set_text(f'Finish, check MP3 in dir: [{saving_dir}]')
        ui.notify(f'Finish, check MP3 in dir: [{saving_dir}]')
    except:
        label_info.style('color: red; margin-top: 10px').set_text('Download fail, pls check URL...')
        ui.notify('Download fail, pls check URL...')

    # enable the items
    enable_GUI_items()


async def async_callback_radio_method():
    # disable the items
    disable_GUI_items()

    # save links input when switch
    global previous_buffer
    saved_link = input_url.value
    input_url.clear()
    input_url.value = previous_buffer
    previous_buffer = saved_link

    label_info.style('color: green; margin-top: 10px').set_text(f'Switch to mode: [{radio_method.value}]')
    ui.notify(f'Switch to {radio_method.value}')
    await asyncio.sleep(1)
    if radio_method_options.index(radio_method.value) == 1:
        label_info.style('color: red; margin-top: 10px').set_text('Downloading the whole playlist will be slow!')
        ui.notify('Downloading the whole playlist will be slow!')
        await asyncio.sleep(2)
    label_info.style('color: green; margin-top: 10px').set_text('Downloader ready...')
    ui.notify('Downloader ready...')

    # enable the items
    enable_GUI_items()


previous_buffer = ''
radio_method_options = ['Single YouTube URL', 'YouTube Playlist URL']

# define GUI items
with ui.card().style('max-width: 800px;').classes('container'):
    with ui.row().style('width: 100%'):
        ui.label("YouTube MP3 Downloader").classes("text-h4 text-center")

    with ui.row().style('width: 100%'):
        radio_method = ui.radio(radio_method_options, value='Single YouTube URL', on_change=async_callback_radio_method).props('inline')
        radio_method.disable()
    with ui.row().style('width: 100%'):
        input_url = ui.input(label="Pls enter YouTube URL",
                             placeholder="https://www.youtube.com/watch?v=example").style('width: 100%;')

with ui.card().style('max-width: 800px;').classes('container'):
    with ui.row().style('width: 100%'):
        ui.label('Save MP3 to...').classes("text-h5 text-center")

    with ui.row().style('width: 100%').classes('justify-between'):
        input_dir = ui.input(label='Directory:', placeholder=DEFAULT_SAVING_DIR).style('width: 85%;')
        button_dir = ui.button('Select', on_click=async_callback_button_dir).style('margin-top: 10px')

    with ui.row().style('width: 100%'):
        label_info = ui.label('Downloader ready...').style('color: green; margin-top: 10px').classes("text-h6 text-center")

    with ui.row().style('width: 100%').classes('justify-end'):
        button_download = ui.button("Download MP3", on_click=async_callback_button_download).style('margin-top: 10px')

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()  # freeze_support() is necessary for pyinstaller
    ui.run(reload=False, port=4655)  # reload=False is necessary for pyinstaller
