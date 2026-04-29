import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path
from PIL import Image, ImageTk
import sys
import os
import json
import urllib.request
import zipfile
import subprocess
import shutil
import base64
from io import BytesIO
from tkinter import messagebox as mb

icon_image_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADr8AAA6/ATgFUyQAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuOWxu2j4AAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAMAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAAdpMAAOgDAAB2kwAA6AMAAFBhaW50Lk5FVCA1LjEuOQADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAAB6K57JJsy6WAAAA/pJREFUeF7t3S+KlVEAh+HvGpwZRjDIZcQqiMswmUWDK9AyUdDmAiwa3IBREMEdGLTIBKtRMCmD/xgEy2c/CzhXeJ8n/vI5L6edzcJO/To4WMdtpr3lwjhNtffn22bcmOfcOAAdAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBhAgBh+b/ZT7ZX1nGb6eT713GaarvdjtNUt4+ujtNUm4/v0nfACwDCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADCBADC0n+j/w9e7e+v4zbTncOjcZpqc/rZGdwhLwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAIEwAI8zf7jl17fmkdt5m+vD8dp6nun78xTlM9e/E2fQe8ACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACBMACAs/Tf6sizLw3s313Gb6c31D+M01acHP/JnoMwLAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAML8Db9jl48vruM20+/Dn+M01dkTZ3CXvAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgTAAgzN/scUePzq3jNtPx31vjNNXjp6/Td8ALAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMIEAMLSf6OzLId3l3XcZjp76QzukhcAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhAkAhP0DGl4q+bMmsRkAAAAASUVORK5CYII=
"""
icon_image_data = base64.b64decode(icon_image_base64)

title_image_base64 = """
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"""
title_image_data = base64.b64decode(title_image_base64)


try:
    jsonreq = urllib.request.Request(
        "https://jacobdrive.pnc3.net/public/api/resources/download?file=%2Favailable.json%2F&algo=tar.gz&hash=KCmam1tiiFGDu1a1V4mkQQ",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    )
    with urllib.request.urlopen(jsonreq) as response, open('available.json', 'wb') as out_file:
        out_file.write(response.read())
except urllib.error.URLError as e:
    mb.showerror("Network Error", f"Network Error; Failed to get versions from server; ERROR: {e.reason}; CAN ONLY USE ALREADY INSTALLED VERSIONS!!!")
    print(f"URL Error: {e.reason}")

try:
    with open('available.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: The file 'data.json' was not found.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the file.")

def open_install_directory():
    path = get_install_directory()
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    try:
        if os.name == "nt":
            os.startfile(path)
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception as e:
        tk.messagebox.showerror("Error", f"Cannot open directory:\n{e}")

def get_install_directory():
    home = Path.home()
    if os.name == "nt":
        return Path(os.getenv("APPDATA")) / "Flintforge"
    else:
        return home / ".local" / "share" / "Flintforge"

def selection_changed(event):
    selected_item = combo_box.get()
    selectedlabel.config(text=f"Selected Version: {selected_item}")

def clear_directory_contents(directory_path):
    p = Path(directory_path)
    if not p.is_dir():
        print(f"Error: {directory_path} is not a valid directory.")
        return

    for item in p.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

def launch_game(versionLocation, versionBinary, platform, version):
    command = [versionBinary]
    if (platform == "linux" and data["versions"][version]["requiresWine"]):
        versionBinary = versionBinary + ".exe"
        command = ["wine", versionBinary]
        if not is_wine_installed():
            mb.showerror("Fatal Error", f"Program WINE is required for {versionBinary}")
            print(f"Error: Program WINE is required for {versionBinary}")
            exit(1)

    if not sys.platform.startswith("win"):
        try:
            os.chmod(versionBinary, 0o755)
        except Exception as e:
            print(f"[WARNING] Failed to chmod binary: {e}")

    if sys.platform.startswith("win"):
        subprocess.Popen(command, cwd=versionLocation, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        os.chmod(versionBinary, 0o755)

        subprocess.Popen([
            "urxvt",
            "-cd", str(versionLocation),
            "-fn", "xft:Monospace:size=10",
            "-e", versionBinary
        ])

def get_first_file_pathlib(directory_path, extension):
    if not extension.startswith('.'):
        extension = '.' + extension
        
    p = Path(directory_path)
    try:
        first_file = next(f for f in p.glob(f"*{extension}") if f.is_file())
        return first_file
    except StopIteration:
        return None

def is_wine_installed():
    try:
        subprocess.check_output(['which', 'wine'])
        return True
    except subprocess.CalledProcessError:
        return False

def is_urxvt_installed():
    return shutil.which("urxvt") is not None

def on_button_click(version):
    home = Path.home()
    if sys.platform.startswith("win"):
        systemType = "win"
        path = Path(os.getenv('APPDATA'))
    else:
        systemType = "linux"
        path = home / ".local" / "share"
    path = path / "Flintforge"
    path.mkdir(parents=True, exist_ok=True)
    versionDeclaredFilePath = Path(path / str(version + ".versiondeclaration"))
    if (versionDeclaredFilePath.is_file()):
        launch_game(str(path), str(Path(path / "FlintforgeCPP")), systemType, version)
        return
    try:
        for file_path in path.glob("*.versiondeclaration"):
            try:
                file_path.unlink()
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
        for value in data["updateRMDIR"]:
            dirPath = Path( path /value )
            if (dirPath.is_dir()): 
                clear_directory_contents(dirPath)
        for value in data["updateRMFILE"]:
            filePath = Path(path / value)
            if (filePath.exists()): 
                filePath.unlink()
    except FileNotFoundError:
        print(f"[WARNING] Failed to delete existing version.")
    local_zipfilename = path / "game.zip"
    url = data["versions"][version][systemType]
    zipreq = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    )
    
    
    for key, value in data["essentialDLL"].items():
        dllreq = urllib.request.Request(
            value,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )
        with urllib.request.urlopen(dllreq) as response, open(str(Path(path / key)), 'wb') as out_file:
            out_file.write(response.read())
    
    with urllib.request.urlopen(zipreq) as response, open(local_zipfilename, 'wb') as out_file:
        out_file.write(response.read())
    with zipfile.ZipFile(local_zipfilename, 'r') as zip_ref:
        zip_ref.extractall(path)
    try:
        local_zipfilename.unlink()
    except FileNotFoundError:
        print(f"[WARNING] Failed to delete {version}'s temporary zip archive.")
    
    versionDeclaredFilePath.touch()
    installedlabel.config(text=f"Installed Version: {version}")
    
    launch_game(str(path), str(Path(path / "FlintforgeCPP")), systemType, version)

    



root = tk.Tk()
root.title("Flintforge Launcher")
root.geometry("600x340")

bgColor = "#222222"
style = ttk.Style()
style.theme_use('default')
style.configure("BW.TLabel", background=bgColor, foreground="white")
style.configure("BW.TCombobox", fieldbackground="black", foreground="white")
style.map("BW.TCombobox",
          fieldbackground=[('readonly', 'black')],
          background=[('readonly', 'white')],
          foreground=[('readonly', 'white')])
root.configure(bg=bgColor)

img = Image.open(BytesIO(title_image_data))
img = img.resize((400, 119), Image.LANCZOS)

tk_image = ImageTk.PhotoImage(img)

label_widget = ttk.Label(root, image=tk_image, style="BW.TLabel")
label_widget.pack(pady=20)

label_widget.image = tk_image

icon_image = Image.open(BytesIO(icon_image_data))
try:
    photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, photo)
except tk.TclError as e:
    print(f"Error loading icon: {e}")

items = list(data['versions'].keys())

hometemp = Path.home()
if sys.platform.startswith("win"):
    systemType = "win"
    pathtemp = Path(os.getenv('APPDATA'))
else:
    systemType = "linux"
    pathtemp = hometemp / ".local" / "share"

if (systemType == "linux"):
    if not is_urxvt_installed():
        mb.showerror("Fatal Error", f"Program urxvt is required for Flintforge Launcher; Fix: install urxvt or rxvt-unicode terminal emulator.")
        print(f"Error: Program urxvt is required and is missing.")
        exit(1)

installedVersion = get_first_file_pathlib(pathtemp / "Flintforge", ".versiondeclaration")
installedVersion_filename = installedVersion.stem if installedVersion else "None"
installedlabel = ttk.Label(root, text=f"Installed Version: {installedVersion_filename}", style="BW.TLabel")
installedlabel.pack(pady=10)

latestVersion = list(data["versions"].keys())[0]
selectedlabel = ttk.Label(root, text=f"Selected Version: {latestVersion}", style="BW.TLabel")
selectedlabel.pack(pady=10)

combo_box = ttk.Combobox(root, values=items, state="readonly", style="BW.TCombobox")
combo_box.pack(pady=10)
combo_box.set(latestVersion)
combo_box.bind("<<ComboboxSelected>>", selection_changed)

button_launch = tk.Button(root, text="Launch", command=lambda: on_button_click(combo_box.get()))
button_launch.pack(pady=5)


open_dir_button = tk.Button(root, text="Open Install Folder", command=open_install_directory)
open_dir_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

root.mainloop()
