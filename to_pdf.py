import os
import win32com.client as win32
import win32gui

base_dir = os.path.dirname(os.path.abspath(__file__))

input_dir = os.path.join(base_dir, 'input')
# output_dir = os.path.join(base_dir, 'output')

hwp_dir = os.path.join(input_dir, 'hwp')
pdf_dir = os.path.join(input_dir, 'pdf')

def hwp_to_pdf():

    os.chdir(hwp_dir)

    hwp = win32.gencache.EnsureDispatch('HWPFrame.HwpObject')
    # hwnd = win32gui.FindWindow(None, 'Noname 1 - HWP')

    # print(hwnd)

    # win32gui.ShowWindow(hwnd, 0)

    for file_name in os.listdir():
        if file_name[-3:] == 'hwp':
            print(f'hwp file : {file_name}')
            hwp.Open(os.path.join(hwp_dir, file_name))
            hwp.SaveAs(f'{pdf_dir}\\{file_name[:-4]}.pdf', 'PDF')

            # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    hwp.Quit()
