# 🎉 Party Manager v2.0 - User Guide

## What is Party Manager?

Party Manager is a Windows application that helps you set up everything for your party invitations in one place!

## Features

✅ **Guest List Management** - Manual entry, CSV uploads, and one-click phone prep  
✅ **Cloud RSVPs** - Fetch guest responses directly from Supabase  
✅ **Party Details** - Fill out form OR upload Canva flyers  
✅ **RSVP Toggle** - Open or close RSVPs with a single checkbox  
✅ **Auto GitHub Push** - Automatically deploys your changes to the web  

---

## Getting Started

### Launch the App
1. Ensure dependencies are installed: `pip install -r requirements.txt`
2. Launch: Double-click `Start_Party_Manager.bat` or run `pythonw party_manager_v2.pyw`

---

## Tab 1: 📋 Guest List Manager

This tab is where you prepare your invitation list.

**Step 1: Upload CSV**
1. Click "📁 Upload CSV File" or drag and drop a CSV anywhere in the window.
2. The preview will show your names and phone numbers.

**Manual Management**
- **Add**: Use the "Add/Edit Guest Manually" box to add people fast. Press **ENTER** to submit.
- **Edit**: Double-click any guest in the list to correct their details.
- **Delete**: Select one or more guests and press the **DELETE** key.

**Step 3 & 4: Prepare for Phone**
1. Click **"✅ Update mobile_sender.html"** (Step 3). This injects your list into the sender file.
2. Click **"💾 Save To..."** (Step 4). Save this file to **Dropbox** or **Google Drive**.
3. Open the file on your phone to start sending invites!

---

## Tab 2: 🎊 Party Details

**Essential Info**
1. Fill out the Event Name, Date, Time, and Location.
2. **RSVP Status**: Check the box to keep RSVPs "Open." Uncheck it to show guests a "closed" message.

**Choose Your Style**
- **📝 Text Mode**: Type a description for a simple, elegant website.
- **🖼️ Image Mode**: Upload a Canva flyer for a high-impact visual.

**Deploy**
1. Click **"🚀 Update & Push to GitHub"**.
2. Your website (index.html) will update live in ~2 minutes!

---

## Tab 3: ☁️ Cloud RSVPs

This tab connects to your Supabase database to see who replied.

1. **Refresh**: Click "🔄 Refresh Events" to find all your past/future parties.
2. **Load**: Select a party and click "📥 Load Guests" to see the full list of replies.
3. **Import**: Click the big green button to move everyone who said **"Yes"** back into your main Guest List Manager (Tab 1). This is perfect for sending text reminders or thank-you notes!

---

## Tab 4: 📨 Email Broadcasts

Need to send a reminder or update to everyone who said "Yes"? Use this tab to blast an email!

1. **Select**: Choose your event to see exactly how many guests you are targeting.
2. **Compose**: Edit the subject and the message body. 
3. **Send**: Click "Send to Confirmed Attendees." The app will loop through your list and send them via **Resend**.

⚠️ **Note**: Ensure your Resend API key is saved in `docs/resend_key`.

---

## Tips & Tricks

- **Keyboard Shortcuts**: Use ENTER to add and DELETE to remove guests.
- **Cloud Saving**: Always save your `mobile_sender.html` to a cloud folder. That way, you don't need to email it—just open the cloud app on your phone!
- **History**: Use the dropdown at the top of Party Details to quickly reload information from your last party.

---

## Workflow for Success

1. ✅ **Tab 3**: Import "Yes" guests from Cloud (to refresh your manager list).
2. ✅ **Tab 4**: Send a broadcast email reminder to those guests.
3. ✅ **Tab 1**: Update `mobile_sender.html` → Save to Cloud for SMS reminders.
4. ✅ **Tab 2**: Update flyer/info if needed → Push to GitHub.

Everything is now automated! 🚀🎊
