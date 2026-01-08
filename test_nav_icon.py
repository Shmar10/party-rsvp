import flet as ft

def main(page: ft.Page):
    try:
        dest = ft.NavigationBarDestination(icon="people", label="Test")
        print("String icon accepted")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ft.app(target=main)
