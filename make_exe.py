import PyInstaller.__main__

PyInstaller.__main__.run([
    'ice_launcher/app.py',
    '--name=ice_launcher',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--add-data=.venv/lib/python3.10/site-packages/customtkinter:customtkinter/',
    '--add-data=.venv/lib/python3.10/site-packages/minecraft_launcher_lib/version.txt:minecraft_launcher_lib/',
])
