import PyInstaller.__main__

PyInstaller.__main__.run([
    'ice_launcher/__main__.py',
    '--name=ice_launcher',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--strip',
    '--add-data=.venv/lib/python3.10/site-packages/customtkinter/assets/themes/blue.json:customtkinter/assets/themes/',
    '--add-data=.venv/lib/python3.10/site-packages/minecraft_launcher_lib/version.txt:minecraft_launcher_lib/',
])
