#!/bin/bash
pyinstaller --onefile --hidden-import='pkg_resources.py2_warn' main.pyw

sudo cp -r assets dist/ && sudo cp -r sound dist/ && sudo cp 04B_19.TTF dist/
cd dist && sudo mv main flappybird
