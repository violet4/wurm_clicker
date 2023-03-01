#!/usr/bin/env python3
import sys
import os
from argparse import ArgumentParser
import time

try:
    import pyautogui
    import numpy as np
except ImportError:
    print("please make sure to `pipenv install`")


this_dir = os.path.dirname(os.path.abspath(__file__))
pipenv_file = os.path.join(this_dir, 'Pipfile')

pipenv_file_contents = """[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
pyautogui = "*"
numpy = "*"

[dev-packages]

[requires]
python_version = "3.10"
"""


def ensure_pipenv_file():
    if os.path.exists(pipenv_file):
        return
    with open(pipenv_file, 'w') as fw:
        print(pipenv_file_contents, file=fw)
    print("please make sure to `pipenv install`")
    sys.exit()


def parse_args():
    ap = ArgumentParser()
    ap.add_argument('seconds', type=int)
    ap.add_argument('type_key', type=str, help='type "click" if you want to click instead')
    ap.add_argument('-c', '--count', default=-1, type=int)
    ap.add_argument('-p', '--percentage', default=25, type=int)

    pargs = ap.parse_args()

    return pargs


def run_main():
    ensure_pipenv_file()
    pargs = parse_args()

    seconds = pargs.seconds
    count = pargs.count
    percentage = pargs.percentage
    type_key = pargs.type_key

    wiggle_seconds = (percentage/100)*seconds

    while count != 0:
        count -= 1
        total_seconds = seconds + np.abs(np.random.normal(scale=wiggle_seconds))
        print(f"sleeping {total_seconds} seconds")
        time.sleep(total_seconds)
        if type_key == 'click':
            pyautogui.click()
        else:
            pyautogui.typewrite(type_key)






if __name__ == '__main__':
    run_main()

