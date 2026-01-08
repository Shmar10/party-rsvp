import flet as ft
import inspect

try:
    with open('tab_sig.txt', 'w') as f:
        f.write(str(inspect.signature(ft.Tab.__init__)))
except Exception as e:
    print(e)
