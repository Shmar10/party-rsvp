import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import os
import subprocess
import re
import shutil
from pathlib import Path

class PartyManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Party Manager")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")
        
        # Get project directory
        self.project_dir = os.getcwd()
        
        # Guest list data
        self.guests = []
        self.csv_path = None
        
        # Party details
        self.event_image_path = None
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_guest_list_tab()
        self.create_party_details_tab()
        
        # Status bar
        self.status_bar = tk.Label(
            root, 
            text="Ready", 
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
        
        # Title
        title = tk.Label(
            tab, 
            text="Guest List Manager", 
            font=("Arial", 18, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=10)
        
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
        
        # Choice frame
        choice_frame = tk.Frame(tab, bg="#f5f5f5")
        choice_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            choice_frame,
            text="Choose how to set up your party:",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5"
        ).pack(anchor='w', pady=(0, 10))
        
        self.detail_choice = tk.StringVar(value="form")
        
        tk.Radiobutton(
            choice_frame,
            text="📝 Fill out form manually",
            variable=self.detail_choice,
            value="form",
            command=self.toggle_detail_mode,
            font=("Arial", 11),
            bg="#f5f5f5",
            cursor="hand2"
        ).pack(anchor='w', pady=5)
        
        tk.Radiobutton(
            choice_frame,
            text="🖼️ Upload event image (from Canva)",
            variable=self.detail_choice,
            value="image",
            command=self.toggle_detail_mode,
            font=("Arial", 11),
            bg="#f5f5f5",
            cursor="hand2"
        ).pack(anchor='w', pady=5)
        
        # Form frame
        self.form_frame = tk.Frame(tab, bg="#f5f5f5")
        self.form_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Event Name
        tk.Label(
            self.form_frame,
            text="Event Name:",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.event_name = tk.Entry(self.form_frame, font=("Arial", 11), width=40)
        self.event_name.grid(row=0, column=1, pady=5, sticky='ew')
        self.event_name.insert(0, "Celebration Night")
        
        # Event Description (Subtitle)
        tk.Label(
            self.form_frame,
            text="Event Description:",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=1, column=0, sticky='nw', pady=5)
        
        self.event_description = tk.Text(self.form_frame, font=("Arial", 11), width=40, height=2, wrap='word')
        self.event_description.grid(row=1, column=1, pady=5, sticky='ew')
        self.event_description.insert('1.0', "Join us for an unforgettable evening of music, drinks, and great company.")
        
        # Date
        tk.Label(
            self.form_frame,
            text="Date:",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        self.event_date = tk.Entry(self.form_frame, font=("Arial", 11), width=40)
        self.event_date.grid(row=2, column=1, pady=5, sticky='ew')
        self.event_date.insert(0, "Saturday, Jan 24th")
        
        # Time
        tk.Label(
            self.form_frame,
            text="Time:",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=3, column=0, sticky='w', pady=5)
        
        self.event_time = tk.Entry(self.form_frame, font=("Arial", 11), width=40)
        self.event_time.grid(row=3, column=1, pady=5, sticky='ew')
        self.event_time.insert(0, "6:00 PM start")
        
        # Location
        tk.Label(
            self.form_frame,
            text="Location:",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).grid(row=4, column=0, sticky='w', pady=5)
        
        self.event_location = tk.Entry(self.form_frame, font=("Arial", 11), width=40)
        self.event_location.grid(row=4, column=1, pady=5, sticky='ew')
        self.event_location.insert(0, "The Martin's Lanai")
        
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
        
        self.image_status = tk.Label(
            self.image_frame,
            text="No image selected",
            font=("Arial", 10),
            fg="#888",
            bg="#f5f5f5"
        )
        self.image_status.pack()
        
        # Push button (always visible)
        push_frame = tk.Frame(tab, bg="#f5f5f5")
        push_frame.pack(pady=20, padx=20)
        
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
        
        if not file_path:
            return
        
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
        """Update index.html and push to GitHub"""
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
            
            # Git operations
            self.update_status("Committing changes...")
            subprocess.run(['git', 'add', 'index.html'], cwd=self.project_dir, check=True)
            subprocess.run(['git', 'add', 'mobile_sender.html'], cwd=self.project_dir, check=True)
            
            if self.event_image_path and self.detail_choice.get() == "image":
                # Copy image to project
                img_dest = os.path.join(self.project_dir, os.path.basename(self.event_image_path))
                shutil.copy2(self.event_image_path, img_dest)
                subprocess.run(['git', 'add', os.path.basename(self.event_image_path)], cwd=self.project_dir, check=True)
            
            subprocess.run(
                ['git', 'commit', '-m', 'Update party details via Party Manager'],
                cwd=self.project_dir,
                check=True
            )
            
            self.update_status("Pushing to GitHub...")
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.project_dir, check=True)
            
            messagebox.showinfo(
                "Success! 🎉",
                "Party details updated and pushed to GitHub!\n\nYour website will be live in ~2 minutes."
            )
            self.update_status("Successfully pushed to GitHub!")
            
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
        
        # Update date
        content = re.sub(
            r'<span>.*?</span>\s*</div>\s*<div class="detail-item">\s*<span class="icon">📅</span>',
            f'<span>{self.event_date.get()}</span></div><div class="detail-item"><span class="icon">📅</span>',
            content,
            count=1
        )
        
        # Update time
        content = re.sub(
            r'<span class="icon">⏰</span>\s*<span>.*?</span>',
            f'<span class="icon">⏰</span><span>{self.event_time.get()}</span>',
            content
        )
        
        # Update location
        content = re.sub(
            r'<span class="icon">📍</span>\s*<span>.*?</span>',
            f'<span class="icon">📍</span><span>{self.event_location.get()}</span>',
            content
        )
        
        return content
    
    def update_with_image(self, content):
        """Update HTML content to display event image"""
        img_filename = os.path.basename(self.event_image_path)
        
        # Replace the event-details section with an image
        image_html = f'''<div class="event-details">
                <img src="{img_filename}" alt="Event Details" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            </div>'''
        
        content = re.sub(
            r'<div class="event-details">.*?</div>',
            image_html,
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = PartyManagerApp(root)
    root.mainloop()
