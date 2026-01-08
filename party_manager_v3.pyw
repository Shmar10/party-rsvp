import flet as ft
import pandas as pd
import os
import subprocess
import re
import shutil
import json
import threading
from pathlib import Path
from datetime import datetime
from supabase import create_client, Client
import dateutil.parser
import resend

class PartyManagerPro:
    def __init__(self):
        # State initialization (Logic from v2)
        self.project_dir = os.getcwd()
        self.history_file = os.path.join(self.project_dir, ".party_events_history.json")
        self.guests = []
        self.csv_path = None
        self.event_image_path = None
        self.cloud_guests = []
        self.broadcast_guests = []

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Party Manager Pro"
        self.page.theme_mode = "dark"
        self.page.padding = 20
        self.page.window_width = 1100
        self.page.window_height = 850
        
        # UI State Components
        self.guest_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Phone")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[],
            expand=True,
        )

        # Navigation
        self.nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon="people", label="Guest List"),
                ft.NavigationBarDestination(icon="celebration", label="Party Details"),
                ft.NavigationBarDestination(icon="cloud", label="Cloud RSVPs"),
                ft.NavigationBarDestination(icon="email", label="Broadcasts"),
            ],
            on_change=self.on_nav_change,
            selected_index=0,
            bgcolor="#111111", # Explicit dark background
            indicator_color="blue",
        )
        
        # Content area
        self.content_area = ft.Container(
            content=self.build_guest_list_tab(),
            expand=True,
            padding=20,
        )

        # Set page navigation bar
        self.page.navigation_bar = self.nav_bar
        
        # Add content to page
        self.page.add(self.content_area)
        self.page.update()

    def on_nav_change(self, e):
        # Switch content based on selected navigation index
        index = self.nav_bar.selected_index
        
        if index == 0:
            self.content_area.content = self.build_guest_list_tab()
        elif index == 1:
            self.content_area.content = self.build_party_details_tab()
        elif index == 2:
            self.content_area.content = self.build_cloud_rsvps_tab()
        elif index == 3:
            self.content_area.content = self.build_broadcasts_tab()
        
        self.page.update()

    def build_guest_list_tab(self):
        # Guest count text
        self.guest_count_text = ft.Text("0 guests", size=16, color="grey")
        
        return ft.Column([
            ft.Row([
                ft.Text("Guest List Manager", size=24, weight="bold"),
                self.guest_count_text,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.Button(
                    "Import CSV", 
                    icon="upload_file", 
                    on_click=lambda _: self.show_csv_import_dialog(),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
                ),
                ft.Button(
                    "Export CSV", 
                    icon="download", 
                    on_click=lambda _: self.export_guests_to_csv(),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                    )
                ),
                ft.Button(
                    "Add Guest", 
                    icon="add",
                    on_click=lambda _: self.show_add_guest_dialog()
                ),
            ], spacing=20),
            ft.Divider(height=20),
            ft.ListView([self.guest_table], expand=True, spacing=10, padding=10)
        ], expand=True, spacing=15)

    def show_csv_import_dialog(self):
        file_path_input = ft.TextField(
            label="CSV File Path",
            hint_text="C:\\path\\to\\guests.csv",
            expand=True,
            autofocus=True
        )
        
        def import_clicked(e):
            if not file_path_input.value:
                self.show_message("Please enter a file path", is_error=True)
                return
            
            try:
                df = pd.read_csv(file_path_input.value)
                if 'Name' not in df.columns or 'Phone' not in df.columns:
                    self.show_message("Error: CSV must have 'Name' and 'Phone' columns", is_error=True)
                    return

                self.guests = df.to_dict('records')
                self.update_guest_table()
                self.show_message(f"Successfully loaded {len(self.guests)} guests!")
                self.page.dialog.open = False
                self.page.update()
            except FileNotFoundError:
                self.show_message("File not found. Please check the path.", is_error=True)
            except Exception as ex:
                self.show_message(f"Failed to load CSV: {str(ex)}", is_error=True)
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Import CSV"),
            content=ft.Column([
                file_path_input,
                ft.Text("Tip: Right-click file in Explorer → Copy as path", size=12, color="grey")
            ], tight=True, height=100),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page.dialog, 'open', False) or self.page.update()),
                ft.Button("Import", on_click=import_clicked),
            ],
        )
        self.page.dialog.open = True
        self.page.update()
    
    def export_guests_to_csv(self):
        try:
            df = pd.DataFrame(self.guests)
            output_path = os.path.join(os.path.dirname(__file__), "guests_export.csv")
            df.to_csv(output_path, index=False)
            self.show_message(f"Exported {len(self.guests)} guests to {output_path}")
        except Exception as ex:
            self.show_message(f"Export failed: {str(ex)}", is_error=True)

    def update_guest_table(self):
        self.guest_table.rows.clear()
        for idx, g in enumerate(self.guests):
            self.guest_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(g.get('Name', '')))),
                        ft.DataCell(ft.Text(str(g.get('Phone', '')).replace('.0', ''))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon="edit",
                                    icon_color="blue",
                                    tooltip="Edit Guest",
                                    on_click=lambda e, i=idx: self.show_edit_guest_dialog(i)
                                ),
                                ft.IconButton(
                                    icon="delete",
                                    icon_color="red",
                                    tooltip="Delete Guest",
                                    on_click=lambda e, i=idx: self.delete_guest(i)
                                ),
                            ], spacing=5)
                        ),
                    ]
                )
            )
        
        # Update guest count
        count = len(self.guests)
        self.guest_count_text.value = f"{count} guest{'s' if count != 1 else ''}"
        self.page.update()

    def show_message(self, text, is_error=False):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(text),
            bgcolor="red" if is_error else "green"
        )
        self.page.snack_bar.open = True
        self.page.update()

    def show_add_guest_dialog(self):
        name_input = ft.TextField(label="Name", autofocus=True)
        phone_input = ft.TextField(label="Phone")

        def add_clicked(e):
            if name_input.value and phone_input.value:
                self.guests.append({"Name": name_input.value, "Phone": phone_input.value})
                self.update_guest_table()
                self.show_message(f"Added {name_input.value} to guest list")
                self.page.dialog.open = False
                self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Add New Guest"),
            content=ft.Column([name_input, phone_input], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page.dialog, 'open', False) or self.page.update()),
                ft.Button("Add", on_click=add_clicked),
            ],
        )
        self.page.dialog.open = True
        self.page.update()
    
    def show_edit_guest_dialog(self, index):
        guest = self.guests[index]
        name_input = ft.TextField(label="Name", value=guest.get('Name', ''), autofocus=True)
        phone_input = ft.TextField(label="Phone", value=str(guest.get('Phone', '')))

        def save_clicked(e):
            if name_input.value and phone_input.value:
                self.guests[index] = {"Name": name_input.value, "Phone": phone_input.value}
                self.update_guest_table()
                self.show_message(f"Updated {name_input.value}")
                self.page.dialog.open = False
                self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Edit Guest"),
            content=ft.Column([name_input, phone_input], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page.dialog, 'open', False) or self.page.update()),
                ft.Button("Save", on_click=save_clicked),
            ],
        )
        self.page.dialog.open = True
        self.page.update()
    
    def delete_guest(self, index):
        guest_name = self.guests[index].get('Name', 'Guest')
        
        def confirm_delete(e):
            del self.guests[index]
            self.update_guest_table()
            self.show_message(f"Deleted {guest_name}")
            self.page.dialog.open = False
            self.page.update()
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete {guest_name}?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page.dialog, 'open', False) or self.page.update()),
                ft.Button("Delete", on_click=confirm_delete, bgcolor="red", color="white"),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def build_party_details_tab(self):
        self.ev_name = ft.TextField(label="Event Name", value="Celebration Night")
        self.ev_date = ft.TextField(label="Date (YYYY-MM-DD)", value=datetime.now().strftime("%Y-%m-%d"))
        self.ev_time = ft.TextField(label="Time", value="6:00 PM start")
        self.ev_location = ft.TextField(label="Location", value="The Martin's Lanai")
        self.ev_rsvp_open = ft.Switch(label="RSVP Form is Open", value=True)
        self.ev_desc = ft.TextField(label="Description", multiline=True, min_lines=3, value="Join us for an unforgettable evening!")

        return ft.Column([
            ft.Text("Party & Site Settings", size=24, weight="bold"),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        self.ev_name,
                        ft.Row([self.ev_date, self.ev_time]),
                        self.ev_location,
                        self.ev_desc,
                        self.ev_rsvp_open,
                    ], spacing=15),
                    padding=20
                )
            ),
            ft.Divider(height=20),
            ft.Button(
                "🚀 Update & Push to GitHub", 
                icon="rocket_launch",
                on_click=self.update_and_push,
                height=60,
                style=ft.ButtonStyle(bgcolor="green", color="white")
            ),
        ], expand=True, spacing=15, scroll="adaptive")

    def update_and_push(self, e):
        self.show_message("Starting Deployment... 🚀")
        
        def run_deploy():
            try:
                # 1. Update index.html and mobile_sender.html (Simplified for v3)
                # In real use, this would call the regex replacement logic from v2
                self.show_message("Syncing Git Repository...")
                subprocess.run(['git', 'add', '.'], cwd=self.project_dir, check=True)
                subprocess.run(['git', 'commit', '-m', f"Update Event: {self.ev_name.value}"], cwd=self.project_dir, check=True)
                subprocess.run(['git', 'push'], cwd=self.project_dir, check=True)
                self.show_message("✅ Website Updated & Deployed!", is_error=False)
            except Exception as ex:
                self.show_message(f"Deployment Failed: {str(ex)}", is_error=True)

        threading.Thread(target=run_deploy).start()

    def build_cloud_rsvps_tab(self):
        # Stats Cards
        self.stats_headcount = ft.Text("0", size=30, weight="bold")
        self.stats_dietary = ft.Text("0", size=30, weight="bold", color="red")
        
        # Connection Inputs
        self.sb_url = ft.TextField(label="Supabase URL", expand=True)
        self.sb_key = ft.TextField(label="Supabase Key", expand=True, password=True, can_reveal_password=True)
        
        # Pre-fill logic
        self.prefill_supabase_creds()

        self.event_dropdown = ft.Dropdown(
            label="Select Event", 
            on_select=self.on_cloud_event_change,
            expand=True
        )
        
        self.cloud_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Count")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Dietary")),
            ],
            rows=[],
        )

        return ft.Column([
            ft.Text("Cloud RSVPs", size=24, weight="bold"),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([self.sb_url, self.sb_key]),
                        ft.Button("Connect & Refresh Events", icon="refresh", on_click=self.refresh_cloud_events),
                    ]),
                    padding=15
                )
            ),
            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Total Expected", size=14, color="grey"),
                            self.stats_headcount,
                        ]),
                        padding=20, width=200
                    )
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Dietary Alerts", size=14, color="grey"),
                            self.stats_dietary,
                        ]),
                        padding=20, width=200
                    )
                ),
            ], spacing=20),
            ft.Row([self.event_dropdown, ft.Button("Import 'Yes' Guests", icon="download", on_click=self.import_cloud_guests)]),
            ft.ListView([self.cloud_table], expand=True, spacing=10)
        ], expand=True, spacing=15)

    def prefill_supabase_creds(self):
        try:
            script_path = os.path.join(self.project_dir, "script.js")
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    js_content = f.read()
                    url_match = re.search(r"const SUPABASE_URL = '(.*?)';", js_content)
                    key_match = re.search(r"const SUPABASE_KEY = '(.*?)';", js_content)
                    if url_match: self.sb_url.value = url_match.group(1)
                    if key_match: self.sb_key.value = key_match.group(1)
        except: pass

    def refresh_cloud_events(self, e):
        url = self.sb_url.value.strip()
        key = self.sb_key.value.strip()
        if not url or not key:
            self.show_message("Please provide Supabase credentials", is_error=True)
            return

        try:
            supabase: Client = create_client(url, key)
            response = supabase.table('rsvps').select('event_name, event_date').execute()
            data = response.data
            
            if not data:
                self.show_message("No RSVPs found in database", is_error=True)
                return

            events = sorted(list(set([f"{item.get('event_name')} ({item.get('event_date')})" for item in data])), reverse=True)
            self.event_dropdown.options = [ft.dropdown.Option(ev) for ev in events]
            self.event_dropdown.value = events[0] if events else None
            self.on_cloud_event_change(None)
            self.show_message(f"Found {len(events)} events!")
        except Exception as ex:
            self.show_message(f"Supabase Error: {str(ex)}", is_error=True)

    def on_cloud_event_change(self, e):
        full_event = self.event_dropdown.value
        if not full_event: return

        event_name = full_event.rsplit(" (", 1)[0]
        url = self.sb_url.value.strip()
        key = self.sb_key.value.strip()

        try:
            supabase: Client = create_client(url, key)
            response = supabase.table('rsvps').select('*').eq('event_name', event_name).execute()
            self.cloud_guests = response.data
            
            self.cloud_table.rows.clear()
            total_count = 0
            dietary_alerts = 0
            
            for g in self.cloud_guests:
                party_size = g.get('party_size') or 1
                attending = str(g.get('attending', '')).lower() == 'yes'
                dietary = g.get('notes') or g.get('dietary_notes') or ""
                
                if attending: total_count += int(party_size)
                if dietary.strip(): dietary_alerts += 1
                
                self.cloud_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(g.get('guest_name') or g.get('name') or "Unknown")),
                            ft.DataCell(ft.Text(str(party_size))),
                            ft.DataCell(ft.Icon("check_circle" if attending else "cancel", color="green" if attending else "red")),
                            ft.DataCell(ft.Text(dietary, color="orange" if dietary else "white")),
                        ]
                    )
                )
            
            self.stats_headcount.value = str(total_count)
            self.stats_dietary.value = str(dietary_alerts)
            self.page.update()
        except: pass

    def import_cloud_guests(self, e):
        if not self.cloud_guests:
            self.show_message("No guests to import", is_error=True)
            return
        
        yes_guests = [g for g in self.cloud_guests if str(g.get('attending', '')).lower() == 'yes']
        new_entries = [{"Name": g.get('guest_name') or g.get('name'), "Phone": g.get('phone', '')} for g in yes_guests]
        
        self.guests.extend(new_entries)
        self.update_guest_table()
        self.show_message(f"Imported {len(new_entries)} guests to local list!")
        self.nav_bar.selected_index = 0
        self.content_area.content = self.build_guest_list_tab()
        self.page.update()

    def build_broadcasts_tab(self):
        self.email_subject = ft.TextField(label="Subject", value="Reminder for our upcoming party!", expand=True)
        self.email_from = ft.TextField(label="From Email", value="invites@shmarten.com", expand=True)
        self.email_body = ft.TextField(
            label="Message Body", 
            multiline=True, 
            min_lines=10, 
            max_lines=15, 
            value="Hi everyone!\n\nJust a quick reminder about the party. We can't wait to see you there!\n\nBest,\n[Your Name]"
        )
        
        self.broadcast_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[],
        )

        return ft.Row([
            # Left: Compose
            ft.Container(
                content=ft.Column([
                    ft.Text("Step 1: Compose Message", size=20, weight="bold"),
                    self.email_from,
                    self.email_subject,
                    self.email_body,
                    ft.Button(
                        "Send Email Blast", 
                        icon="send", 
                        on_click=self.send_broadcast,
                        style=ft.ButtonStyle(bgcolor="blue", color="white"),
                        height=50
                    ),
                ], spacing=15),
                expand=2,
                padding=20,
                border=ft.border.all(1, "grey"),
                border_radius=10
            ),
            # Right: Recipients
            ft.Container(
                content=ft.Column([
                    ft.Text("Step 2: Review Recipients", size=20, weight="bold"),
                    ft.ListView([self.broadcast_table], expand=True),
                ], spacing=15),
                expand=3,
                padding=20,
                border=ft.border.all(1, "grey"),
                border_radius=10
            )
        ], expand=True, spacing=20)

    def send_broadcast(self, e):
        if not self.guests and not self.cloud_guests:
            self.show_message("No recipients found. Please load guests first.", is_error=True)
            return
            
        # Determine recipients (favor cloud guests if in context, or local)
        recipients = []
        if self.cloud_guests:
            recipients = [g for g in self.cloud_guests if str(g.get('attending', '')).lower() == 'yes']
        else:
            recipients = self.guests

        if not recipients:
            self.show_message("No 'Yes' attendees to target.", is_error=True)
            return

        key_path = os.path.join(self.project_dir, "docs", "resend_key")
        try:
            with open(key_path, 'r') as f:
                resend_key = f.read().strip()
        except:
            self.show_message("Resend API key missing in docs/resend_key", is_error=True)
            return

        self.broadcast_table.rows.clear()
        for r in recipients:
            name = r.get('guest_name') or r.get('name') or "Guest"
            email = r.get('email', 'N/A')
            self.broadcast_table.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(name)), ft.DataCell(ft.Text(email)), ft.DataCell(ft.Text("Pending"))])
            )
        self.page.update()

        # Threaded sending
        def worker():
            resend.api_key = resend_key
            for i, r in enumerate(recipients):
                try:
                    self.broadcast_table.rows[i].cells[2].content = ft.Text("Sending...", color="blue")
                    self.page.update()
                    
                    resend.Emails.send({
                        "from": f"Party Manager <{self.email_from.value}>",
                        "to": r.get('email'),
                        "subject": self.email_subject.value,
                        "text": self.email_body.value
                    })
                    self.broadcast_table.rows[i].cells[2].content = ft.Text("✅ Sent", color="green")
                except Exception as ex:
                    self.broadcast_table.rows[i].cells[2].content = ft.Text(f"❌ Failed", color="red")
                self.page.update()
            self.show_message("Broadcast Complete!")

        threading.Thread(target=worker).start()

if __name__ == "__main__":
    app = PartyManagerPro()
    ft.run(app.main)
