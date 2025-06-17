
import pyautogui as pag 
import subprocess

class Engine:

    def close(self):
        pag.hotkey('Alt', 'F4')

    def open (self, app_name: str):
        pag.press('win')
        pag.write(app_name, interval=0.50)
        pag.press('enter')

    def write(self, text: str)->None:
        pag.write(text, interval= 0.50)

    def shut_down(self):
        subprocess.run('shutdown now')

    def desktop(self, num:str) -> None:
        pag.hotkey('ctrl', f'f{num}')

    def move(self, direction):
        pag.press(direction)
