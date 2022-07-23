import PyInstaller.__main__
import os
import importlib
import platform

minecraft_launcher_lib_root = os.path.dirname(importlib.import_module("minecraft_launcher_lib").__file__)  # type: ignore
version_txt = os.path.join(minecraft_launcher_lib_root, "version.txt")
minecraft_launcher_lib_data = f"--add-data={version_txt}:minecraft_launcher_lib/"
if platform.system() == "Windows":
    minecraft_launcher_lib_data = minecraft_launcher_lib_data.replace("/", "\\")
    minecraft_launcher_lib_data = minecraft_launcher_lib_data.replace(":", ";")

customtkinter_root = os.path.dirname(importlib.import_module("customtkinter").__file__)  # type: ignore
blue_json = os.path.join(customtkinter_root, "assets/themes/blue.json")
customtkinter_data = f"--add-data={blue_json}:customtkinter/assets/themes/"
if platform.system() == "Windows":
    customtkinter_data = customtkinter_data.replace("/", "\\")
    customtkinter_data = customtkinter_data.replace(":", ";")

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
        minecraft_launcher_lib_data,
        customtkinter_data,
    ]
)
