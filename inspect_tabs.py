import flet as ft
import inspect

try:
    with open('tabs_sig.txt', 'w') as f:
        f.write(str(inspect.signature(ft.Tabs.__init__)))
except Exception as e:
    print(e)
