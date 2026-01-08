import flet as ft
import inspect

try:
    with open('navdest_sig.txt', 'w') as f:
        f.write(str(inspect.signature(ft.NavigationBarDestination.__init__)))
except Exception as e:
    print(e)
