import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkcalendar import DateEntry
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import os
import subprocess
import re
import shutil
import json
import threading
from pathlib import Path
from datetime import datetime

class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="#333",
            foreground="white",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9),
            padx=8,
            pady=4
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class PartyManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Party Manager v2.0")
        self.root.geometry("950x750")
        self.root.configure(bg="#f5f5f5")
        
        # Get project directory
        self.project_dir = os.getcwd()
        
        # Event history file
        self.history_file = os.path.join(self.project_dir, ".party_events_history.json")
        
        # Guest list data
        self.guests = []
        self.csv_path = None
        
        # Party details
        self.event_image_path = None
        
        # Progress dialog
        self.progress_window = None
        self.progress_bar = None
        self.progress_label = None
        
        # RSVP status
        self.rsvp_open = tk.BooleanVar(value=True)
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_guest_list_tab()
        self.create_party_details_tab()
        
        # Load event history
        self.load_event_history()
        
        # Status bar with timestamp
        self.status_bar = tk.Label(
            root, 
            text="Ready | Party Manager v2.0", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#667eea",
            fg="white",
            font=("Arial", 10)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_guest_list_tab(self):
        """Tab 1: Guest List Manager"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📋 Guest List Manager")
        
        # Enable drag and drop on the entire tab
        try:
            tab.drop_target_register(DND_FILES)
            tab.dnd_bind('<<Drop>>', self.handle_csv_drop)
        except:
            pass  # Drag and drop not available
        
        # Title
        title = tk.Label(
            tab, 
            text="Guest List Manager", 
            font=("Arial", 18, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=10)
        
        # Drag and drop hint
        drag_hint = tk.Label(
            tab,
            text="💡 Tip: Drag and drop your CSV file anywhere in this window!",
            font=("Arial", 10, "italic"),
            fg="#667eea",
            bg="#f5f5f5"
        )
        drag_hint.pack()
        
        # Upload CSV Section
        upload_frame = tk.Frame(tab, bg="#f5f5f5")
        upload_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            upload_frame, 
            text="Step 1: Upload Guest List (CSV)", 
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        ).pack(anchor='w')
        
        upload_btn = tk.Button(
            upload_frame,
            text="📁 Upload CSV File",
            command=self.upload_csv,
            bg="#667eea",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        upload_btn.pack(anchor='w', pady=5)
        ToolTip(upload_btn, "Select your guests.csv file with Name and Phone columns")
        
        self.csv_status = tk.Label(
            upload_frame,
            text="No file selected",
            font=("Arial", 10),
            fg="#888",
            bg="#f5f5f5"
        )
        self.csv_status.pack(anchor='w')
        
        # Guest List Preview
        preview_frame = tk.Frame(tab, bg="#f5f5f5")
        preview_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(
            preview_frame,
            text="Step 2: Preview Guest List",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        ).pack(anchor='w')
        
        # Create treeview for guest list
        columns = ('Name', 'Phone')
        self.guest_tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.guest_tree.heading(col, text=col)
            self.guest_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.guest_tree.yview)
        self.guest_tree.configure(yscroll=scrollbar.set)
        
        self.guest_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Action Buttons
        action_frame = tk.Frame(tab, bg="#f5f5f5")
        action_frame.pack(pady=20, padx=20, fill='x')
        
        tk.Label(
            action_frame,
            text="Step 3: Update mobile_sender.html",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        ).pack(anchor='w', pady=(0, 10))
        
        btn_frame = tk.Frame(action_frame, bg="#f5f5f5")
        btn_frame.pack(anchor='w')
        
        update_btn = tk.Button(
            btn_frame,
            text="✅ Update mobile_sender.html",
            command=self.update_mobile_sender,
            bg="#28a745",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        update_btn.pack(side=tk.LEFT, padx=(0, 10))
        ToolTip(update_btn, "Inject guest list into mobile_sender.html for sending")
        
        save_btn = tk.Button(
            btn_frame,
            text="💾 Save To...",
            command=self.save_mobile_sender,
            bg="#17a2b8",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT)
        ToolTip(save_btn, "Save updated mobile_sender.html to a location of your choice")
    
    def create_party_details_tab(self):
        """Tab 2: Party Details"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🎊 Party Details")
        
        # Title
        title = tk.Label(
            tab,
            text="Party Details Manager",
            font=("Arial", 18, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=10)
        
        # Recent Events Dropdown
        if hasattr(self, 'event_history') and self.event_history:
            history_frame = tk.Frame(tab, bg="#f5f5f5")
            history_frame.pack(pady=5, padx=20, fill='x')
            
            tk.Label(
                history_frame,
                text="📚 Load from Recent Events:",
                font=("Arial", 11, "bold"),
                bg="#f5f5f5"
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            event_names = [e['name'] for e in self.event_history[:10]]
            self.history_var = tk.StringVar()
            
            history_dropdown = ttk.Combobox(
                history_frame,
                textvariable=self.history_var,
                values=event_names,
                state='readonly',
                width=40
            )
            history_dropdown.pack(side=tk.LEFT)
            history_dropdown.bind('<<ComboboxSelected>>', self.on_history_selected)
            ToolTip(history_dropdown, "Select a previous party to load all its details")
        
        # Essential Event Info - ALWAYS VISIBLE (needed for calendar/tracking)
        info_frame = tk.Frame(tab, bg="#f5f5f5")
        info_frame.pack(pady=10, padx=20, fill='x')
        
        # Event Name
        tk.Label(
            info_frame,
            text="Event Name (Required for Tracking):",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.event_name = tk.Entry(info_frame, font=("Arial", 11), width=50)
        self.event_name.grid(row=0, column=1, pady=5, sticky='ew')
        self.event_name.insert(0, "Celebration Night")
        ToolTip(self.event_name, "This name is used to track RSVPs for your event")
        
        # Date
        tk.Label(
            info_frame,
            text="Date (for Calendar):",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.event_date = DateEntry(
            info_frame,
            font=("Arial", 11),
            width=37,
            background='#667eea',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.event_date.grid(row=1, column=1, pady=5, sticky='ew')
        ToolTip(self.event_date, "Used to generate the 'Add to Calendar' link for guests")

        # Time
        tk.Label(
            info_frame,
            text="Time (for Calendar):",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        self.event_time = tk.Entry(info_frame, font=("Arial", 11), width=50)
        self.event_time.grid(row=2, column=1, pady=5, sticky='ew')
        self.event_time.insert(0, "6:00 PM start")
        ToolTip(self.event_time, "Visible in the calendar invite")

        # Location
        tk.Label(
            info_frame,
            text="Location (for Calendar):",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=3, column=0, sticky='w', pady=5)
        
        self.event_location = tk.Entry(info_frame, font=("Arial", 11), width=50)
        self.event_location.grid(row=3, column=1, pady=5, sticky='ew')
        self.event_location.insert(0, "The Martin's Lanai")
        ToolTip(self.event_location, "Location for the calendar invite")
        
        # RSVP Open Toggle
        tk.Label(
            info_frame,
            text="RSVP Status:",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=4, column=0, sticky='w', pady=5)
        
        self.rsvp_toggle = tk.Checkbutton(
            info_frame,
            text="RSVP Form is Open & Accepting Responses",
            variable=self.rsvp_open,
            font=("Arial", 11),
            bg="#f5f5f5",
            activebackground="#f5f5f5",
            cursor="hand2"
        )
        self.rsvp_toggle.grid(row=4, column=1, pady=5, sticky='w')
        ToolTip(self.rsvp_toggle, "Uncheck this to temporarily disable the RSVP form on your website")
        
        info_frame.columnconfigure(1, weight=1)

        # Separator
        ttk.Separator(tab, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Choice frame
        choice_frame = tk.Frame(tab, bg="#f5f5f5")
        choice_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            choice_frame,
            text="Choose how to display details on your page:",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        ).pack(anchor='w', pady=(0, 10))
        
        self.detail_choice = tk.StringVar(value="form")
        
        tk.Radiobutton(
            choice_frame,
            text="📝 Show text details and description",
            variable=self.detail_choice,
            value="form",
            command=self.toggle_detail_mode,
            font=("Arial", 11),
            bg="#f5f5f5",
            cursor="hand2"
        ).pack(anchor='w', pady=5)
        
        tk.Radiobutton(
            choice_frame,
            text="🖼️ Show event image (PNG, JPG, etc.)",
            variable=self.detail_choice,
            value="image",
            command=self.toggle_detail_mode,
            font=("Arial", 11),
            bg="#f5f5f5",
            cursor="hand2"
        ).pack(anchor='w', pady=5)
        
        # Form frame (for manual entry fields)
        self.form_frame = tk.Frame(tab, bg="#f5f5f5")
        self.form_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Event Description (Subtitle)
        tk.Label(
            self.form_frame,
            text="Event Description:",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=1, column=0, sticky='nw', pady=5)
        
        self.event_description = tk.Text(self.form_frame, font=("Arial", 11), width=45, height=3, wrap='word')
        self.event_description.grid(row=1, column=1, pady=5, sticky='ew')
        self.event_description.insert('1.0', "Join us for an unforgettable evening of music, drinks, and great company.")
        
        self.form_frame.columnconfigure(1, weight=1)
        
        # Image frame (hidden by default)
        self.image_frame = tk.Frame(tab, bg="#f5f5f5")
        
        upload_img_btn = tk.Button(
            self.image_frame,
            text="🖼️ Upload Event Image",
            command=self.upload_event_image,
            bg="#667eea",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        upload_img_btn.pack(pady=20)
        ToolTip(upload_img_btn, "Select a Canva image with all event details")
        
        self.image_status = tk.Label(
            self.image_frame,
            text="No image selected",
            font=("Arial", 10),
            fg="#888",
            bg="#f5f5f5"
        )
        self.image_status.pack()
        
        # Push button frame (always at bottom, always visible)
        push_frame = tk.Frame(tab, bg="#f5f5f5")
        push_frame.pack(side=tk.BOTTOM, pady=20, padx=20)
        
        self.push_btn = tk.Button(
            push_frame,
            text="🚀 Update & Push to GitHub",
            command=self.update_and_push,
            bg="#28a745",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=15,
            cursor="hand2"
        )
        self.push_btn.pack()
        ToolTip(self.push_btn, "Update index.html and deploy to your website (saves to history)")
    
    def toggle_detail_mode(self):
        """Toggle between form and image mode"""
        if self.detail_choice.get() == "form":
            self.image_frame.pack_forget()
            self.form_frame.pack(pady=10, padx=20, fill='both', expand=True)
        else:
            self.form_frame.pack_forget()
            self.image_frame.pack(pady=10, padx=20, fill='both', expand=True)
    
    def upload_csv(self):
        """Upload and parse CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Guest List CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_csv_file(file_path)
    
    def update_mobile_sender(self):
        """Update mobile_sender.html with guest data"""
        if not self.guests:
            messagebox.showwarning("No Guests", "Please upload a CSV file first")
            return
        
        try:
            mobile_sender_path = os.path.join(self.project_dir, "mobile_sender.html")
            
            if not os.path.exists(mobile_sender_path):
                messagebox.showerror("File Not Found", "mobile_sender.html not found in project directory")
                return
            
            # Read the file
            with open(mobile_sender_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate guest array
            guest_entries = []
            for guest in self.guests:
                name = guest.get('Name', '').replace('"', '\\"')
                phone = str(guest.get('Phone', '')).replace('.0', '')
                guest_entries.append(f'            {{ name: "{name}", phone: "{phone}" }}')
            
            guest_array = ',\n'.join(guest_entries)
            
            # Replace the guests array
            pattern = r'const guests = \[(.*?)\];'
            replacement = f'const guests = [\n{guest_array}\n        ];'
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # Replace the EVENT_ID
            event_id = self.event_name.get()
            new_content = re.sub(
                r'const EVENT_ID = ".*?";',
                f'const EVENT_ID = "{event_id}";',
                new_content
            )
            
            # Write back
            with open(mobile_sender_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            messagebox.showinfo(
                "Success",
                f"mobile_sender.html updated with {len(self.guests)} guests!"
            )
            self.update_status("mobile_sender.html updated")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update mobile_sender.html:\n{str(e)}")
    
    def save_mobile_sender(self):
        """Save mobile_sender.html to a chosen location"""
        if not self.guests:
            messagebox.showwarning("No Guests", "Please upload a CSV file and update first")
            return
        
        save_path = filedialog.asksaveasfilename(
            title="Save mobile_sender.html",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialfile="mobile_sender.html"
        )
        
        if not save_path:
            return
        
        try:
            source = os.path.join(self.project_dir, "mobile_sender.html")
            shutil.copy2(source, save_path)
            
            messagebox.showinfo(
                "Saved",
                f"mobile_sender.html saved to:\n{save_path}"
            )
            self.update_status(f"Saved to {os.path.basename(save_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def upload_event_image(self):
        """Upload event image"""
        file_path = filedialog.askopenfilename(
            title="Select Event Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.event_image_path = file_path
            self.image_status.config(
                text=f"✅ {os.path.basename(file_path)}",
                fg="#28a745"
            )
            self.update_status(f"Event image selected: {os.path.basename(file_path)}")
    
    def update_and_push(self):
        """Update index.html and push to GitHub with progress bar"""
        try:
            index_path = os.path.join(self.project_dir, "index.html")
            
            if not os.path.exists(index_path):
                messagebox.showerror("File Not Found", "index.html not found")
                return
            
            # Read index.html
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if self.detail_choice.get() == "form":
                # Update with form data
                content = self.update_with_form_data(content)
            else:
                # Update with image
                if not self.event_image_path:
                    messagebox.showwarning("No Image", "Please upload an event image first")
                    return
                content = self.update_with_image(content)
            
            # Write back
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update script.js with RSVP status
            self.update_script_js()
            
            # Show progress and start threaded git operations
            self.show_progress("Deploying to GitHub...")
            self.threaded_git_push()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update:\n{str(e)}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Git Error", f"Git operation failed:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update:\n{str(e)}")
    
    def update_with_form_data(self, content):
        """Update HTML content with form data"""
        event_name_value = self.event_name.get()
        
        # Update data-event-name attribute on main container
        content = re.sub(
            r'<main class="container"[^>]*>',
            f'<main class="container" data-event-name="{event_name_value}">',
            content
        )
        
        # Update event name
        content = re.sub(
            r'<h1 class="glitch-text">.*?</h1>',
            f'<h1 class="glitch-text">{event_name_value}</h1>',
            content
        )
        
        # Update event description (subtitle)
        description = self.event_description.get('1.0', 'end-1c')
        content = re.sub(
            r'<p class="subtitle">.*?</p>',
            f'<p class="subtitle">{description}</p>',
            content
        )
        
        # Format date
        date_obj = self.event_date.get_date()
        formatted_date = date_obj.strftime('%A, %b %d').replace(' 0', ' ')
        day = date_obj.day
        suffix = "th" if 4 <= day <= 20 or 24 <= day <= 30 else ["st", "nd", "rd"][day % 10 - 1]
        formatted_date = formatted_date + suffix

        # Replace the entire event-details section with a clean text version
        # This removes any previously uploaded image and ensures items are visible
        details_html = f'''<div class="event-details">
                <div class="detail-item">
                    <span class="icon">📅</span><span>{formatted_date}</span>
                </div>
                <div class="detail-item">
                    <span class="icon">⏰</span><span>{self.event_time.get()}</span>
                </div>
                <div class="detail-item">
                    <span class="icon">📍</span><span>{self.event_location.get()}</span>
                </div>
            </div>'''
        
        # Robust replacement that cleans up the hero section
        content = re.sub(
            r'<div class="event-details">.*?</header>',
            f'{details_html}\n        </header>',
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def update_with_image(self, content):
        """Update HTML content to display event image with hidden metadata for calendar"""
        img_filename = os.path.basename(self.event_image_path)
        event_name_value = self.event_name.get()
        
        # Format date for metadata
        date_obj = self.event_date.get_date()
        formatted_date = date_obj.strftime('%A, %b %d').replace(' 0', ' ')
        day = date_obj.day
        suffix = "th" if 4 <= day <= 20 or 24 <= day <= 30 else ["st", "nd", "rd"][day % 10 - 1]
        formatted_date = formatted_date + suffix

        # Update data-event-name attribute on main container
        content = re.sub(
            r'<main class="container"[^>]*>',
            f'<main class="container" data-event-name="{event_name_value}">',
            content
        )
        
        # Clear event description (subtitle) in image mode
        content = re.sub(
            r'<p class="subtitle">.*?</p>',
            '<p class="subtitle"></p>',
            content
        )
        
        # Replace the entire event-details section including any stray items after it
        # This regex eats everything until the rsvp-card starts to ensure a clean slate
        image_html = f'''<div class="event-details">
                <img src="{img_filename}" alt="Event Details" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                <div class="detail-item" style="display: none;">
                    <span class="icon">📅</span><span>{formatted_date}</span>
                </div>
                <div class="detail-item" style="display: none;">
                    <span class="icon">⏰</span><span>{self.event_time.get()}</span>
                </div>
                <div class="detail-item" style="display: none;">
                    <span class="icon">📍</span><span>{self.event_location.get()}</span>
                </div>
            </div>'''
        
        # Robust replacement that cleans up the hero section
        content = re.sub(
            r'<div class="event-details">.*?</header>',
            f'{image_html}\n        </header>',
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def update_script_js(self):
        """Update RSVP_OPEN constant in script.js"""
        try:
            script_path = os.path.join(self.project_dir, "script.js")
            if not os.path.exists(script_path):
                return
            
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update RSVP_OPEN constant
            state = "true" if self.rsvp_open.get() else "false"
            new_content = re.sub(
                r'const RSVP_OPEN = (true|false);',
                f'const RSVP_OPEN = {state};',
                content
            )
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            print(f"Error updating script.js: {e}")

    def update_status(self, message):
        """Update status bar with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_bar.config(text=f"{message} | {timestamp}")
        self.root.update_idletasks()
    
    # ===== EVENT HISTORY METHODS =====
    
    def load_event_history(self):
        """Load recent events from JSON file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.event_history = json.load(f)
            except:
                self.event_history = []
        else:
            self.event_history = []
    
    def save_event_to_history(self):
        """Save current event details to history"""
        event_data = {
            "name": self.event_name.get(),
            "description": self.event_description.get('1.0', 'end-1c'),
            "date": self.event_date.get(),
            "time": self.event_time.get(),
            "location": self.event_location.get(),
            "rsvp_open": self.rsvp_open.get(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to beginning of list
        self.event_history.insert(0, event_data)
        
        # Keep only last 10
        self.event_history = self.event_history[:10]
        
        # Save to file
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.event_history, f, indent=2)
        except Exception as e:
            print(f"Could not save history: {e}")
    
    def load_event_from_history(self, event):
        """Load event details from history"""
        self.event_name.delete(0, tk.END)
        self.event_name.insert(0, event.get("name", ""))
        
        self.event_description.delete('1.0', tk.END)
        self.event_description.insert('1.0', event.get("description", ""))
        
        # Set date if valid
        try:
            date_str = event.get("date", "")
            if date_str:
                self.event_date.set_date(date_str)
        except:
            pass
        
        self.event_time.delete(0, tk.END)
        self.event_time.insert(0, event.get("time", ""))
        
        self.event_location.delete(0, tk.END)
        self.event_location.insert(0, event.get("location", ""))
        
        self.rsvp_open.set(event.get("rsvp_open", True))
        
        self.update_status("Event loaded from history")
    
    # ===== PROGRESS BAR METHODS =====
    
    def show_progress(self, title="Processing..."):
        """Show progress dialog"""
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title(title)
        self.progress_window.geometry("400x150")
        self.progress_window.configure(bg="#f5f5f5")
        self.progress_window.resizable(False, False)
        
        # Center on parent
        self.progress_window.transient(self.root)
        self.progress_window.grab_set()
        
        # Label
        self.progress_label = tk.Label(
            self.progress_window,
            text="Starting...",
            font=("Arial", 11),
            bg="#f5f5f5"
        )
        self.progress_label.pack(pady=20)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_window,
            length=350,
            mode='indeterminate'
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)
        
        self.progress_window.update()
    
    def update_progress(self, message):
        """Update progress message (must be called via root.after if from thread)"""
        if self.progress_label:
            self.progress_label.config(text=message)
    
    def hide_progress(self):
        """Hide progress dialog"""
        if self.progress_window:
            self.progress_window.destroy()
            self.progress_window = None
            self.progress_bar = None
            self.progress_label = None
    
    # ===== DRAG AND DROP METHODS =====
    
    def handle_csv_drop(self, event):
        """Handle CSV file drop"""
        file_path = event.data
        
        # Clean up the path (remove curly braces if present)
        file_path = file_path.strip('{}')
        
        if file_path.lower().endswith('.csv'):
            self.load_csv_file(file_path)
        else:
            messagebox.showwarning("Invalid File", "Please drop a CSV file")
    
    def load_csv_file(self, file_path):
        """Load CSV file (used by both upload and drag-drop)"""
        try:
            df = pd.read_csv(file_path)
            
            # Validate columns
            if 'Name' not in df.columns or 'Phone' not in df.columns:
                messagebox.showerror(
                    "Invalid CSV",
                    "CSV must have 'Name' and 'Phone' columns"
                )
                return
            
            self.csv_path = file_path
            self.guests = df.to_dict('records')
            
            # Clear and populate treeview
            for item in self.guest_tree.get_children():
                self.guest_tree.delete(item)
            
            for guest in self.guests:
                name = guest.get('Name', '')
                phone = str(guest.get('Phone', '')).replace('.0', '')
                self.guest_tree.insert('', 'end', values=(name, phone))
            
            self.csv_status.config(
                text=f"✅ {len(self.guests)} guests loaded from {os.path.basename(file_path)}",
                fg="#28a745"
            )
            self.update_status(f"Loaded {len(self.guests)} guests")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV:\n{str(e)}")
    
    # ===== THREADED GIT PUSH =====
    
    def threaded_git_push(self):
        """Run Git operations in a thread"""
        def git_operations():
            try:
                self.root.after(0, lambda: self.update_progress("Adding files to Git..."))
                subprocess.run(['git', 'add', 'index.html'], cwd=self.project_dir, check=True, capture_output=True, timeout=30)
                subprocess.run(['git', 'add', 'mobile_sender.html'], cwd=self.project_dir, check=True, capture_output=True, timeout=30)
                
                if self.event_image_path and self.detail_choice.get() == "image":
                    img_filename = os.path.basename(self.event_image_path)
                    img_dest = os.path.normpath(os.path.join(self.project_dir, img_filename))
                    img_src = os.path.normpath(self.event_image_path)
                    
                    if img_src != img_dest:
                        self.root.after(0, lambda: self.update_progress(f"Copying image: {img_filename}..."))
                        try:
                            shutil.copy2(img_src, img_dest)
                        except Exception as copy_err:
                            self.root.after(0, lambda: self.update_status(f"Warning: Image copy skip/fail: {copy_err}"))
                    
                    subprocess.run(['git', 'add', img_filename], cwd=self.project_dir, check=True, capture_output=True, timeout=30)
                
                self.root.after(0, lambda: self.update_progress("Committing changes..."))
                subprocess.run(
                    ['git', 'commit', '-m', f"Update party details for {self.event_name.get()} via v2"],
                    cwd=self.project_dir,
                    check=True,
                    capture_output=True,
                    timeout=30
                )
                
                self.root.after(0, lambda: self.update_progress("Pushing to GitHub (this may take a moment)..."))
                subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.project_dir, check=True, capture_output=True, timeout=60)
                
                # Save to history
                self.save_event_to_history()
                
                # Success
                self.root.after(0, self.git_push_success)
                
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode() if e.stderr else str(e)
                self.root.after(0, lambda: self.git_push_error(error_msg))
            except Exception as e:
                self.root.after(0, lambda: self.git_push_error(str(e)))
        
        # Start thread
        thread = threading.Thread(target=git_operations, daemon=True)
        thread.start()
    
    def git_push_success(self):
        """Called when Git push succeeds"""
        self.hide_progress()
        messagebox.showinfo(
            "Success! 🎉",
            "Party details updated and pushed to GitHub!\n\nYour website will be live in ~2 minutes."
        )
        self.update_status("Successfully pushed to GitHub!")
    
    def git_push_error(self, error_msg):
        """Called when Git push fails"""
        self.hide_progress()
        messagebox.showerror("Git Error", f"Git operation failed:\n{error_msg}")
        self.update_status("Git push failed")
    
    def on_history_selected(self, event=None):
        """Handle recent event selection"""
        selected_name = self.history_var.get()
        for event in self.event_history:
            if event['name'] == selected_name:
                self.load_event_from_history(event)
                break


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PartyManagerApp(root)
    root.mainloop()
