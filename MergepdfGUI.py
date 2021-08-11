from PyPDF2 import PdfFileMerger
import argparse
from glob import glob
import os
import threading
import time

import PySimpleGUI as sg

DEFAULT_FONT = 'NotoSansCJKkr-Medium'
THREAD_EVENT = '-MERGE_THREAD-'


def merge_pdf(window, src, des, target_string, filename):
    merger = PdfFileMerger()

    for str in target_string:
        for f in glob(f'{src}/*{str}*.pdf'):
            merger.append(f)

    merger.write(f'{des}/{filename}.pdf')
    merger.close()
    window.write_event_value('-THREAD-', (threading.current_thread().name, i))


def main():
    sg.theme('Dark Blue 3')   # Add a touch of color

    layout = [
        [sg.InputText('src folder'), sg.FolderBrowse('select')],
        [sg.InputText('des folder'), sg.FolderBrowse('select')],
        [sg.InputText('string to include')],
        [sg.InputText('target filename')],
        [sg.Multiline('', size=(50, 10))],
        [sg.Button('Stop'), sg.Button('Merge')],
    ]

    window = sg.Window('PDF merger', layout, font=DEFAULT_FONT)

    while True:
        event, values = window.read()

        print('Event : ', event)
        print('Values : ', values)

        src_path = values[0]
        des_path = values[1]
        target_string = values[2].split(',')
        target_filename = values[3]

        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == 'Merge':
            threading.Thread(target=merge_pdf, args=(
                window, src_path, des_path, target_string, target_filename), daemon=True).start()
        if event == 'Stop':
            pass
        if event == THREAD_EVENT:
            print(values[THREAD_EVENT])
            sg.popup_auto_close('merge success!', title='merge result')

    window.close()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-d', '--directory',
    #                     help='directory where files to be merged live')
    # parser.add_argument('bookname')
    # args = parser.parse_args()

    main()
