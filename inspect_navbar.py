import flet as ft
import inspect

try:
    with open('navbar_sig.txt', 'w') as f:
        f.write(str(inspect.signature(ft.NavigationBar.__init__)))
except Exception as e:
    print(e)
