#!/bin/bash
source .venv/bin/activate
pyinstaller --collect-all tkinterdnd2 --collect-all PIL --icon=icon.ico launcher.pyw