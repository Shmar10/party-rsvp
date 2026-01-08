import flet as ft

def main(page: ft.Page):
    page.title = "Button Test"
    
    def button_clicked(e):
        print("Button clicked!")
        page.add(ft.Text("Button works!"))
        page.update()
    
    page.add(
        ft.Button("Test Button", on_click=button_clicked),
        ft.ElevatedButton("Test ElevatedButton", on_click=button_clicked),
    )

ft.app(main)
