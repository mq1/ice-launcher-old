import PyInstaller.__main__


PyInstaller.__main__.run(
    [
        "ice_launcher/__main__.py",
        "--name=Ice Launcher",
        "--clean",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--strip",
        "--noupx",
        "--icon=ice-launcher.png",
        "--collect-data=minecraft_launcher_lib",
        "--collect-data=customtkinter",
    ]
)
