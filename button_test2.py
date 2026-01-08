import flet as ft

def main(page: ft.Page):
    page.title = "Simple Test"
    
    def on_button_click(e):
        print("Button clicked!")
        page.snack_bar = ft.SnackBar(content=ft.Text("Button works!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()
    
    page.add(
        ft.Button("Test ft.Button", on_click=on_button_click),
    )

if __name__ == "__main__":
    ft.app(target=main)
