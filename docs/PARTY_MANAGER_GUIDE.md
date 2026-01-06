# 🎉 Party Manager - User Guide

## What is Party Manager?

Party Manager is a Windows application that helps you set up everything for your party invitations in one place!

## Features

✅ **Guest List Management** - Upload CSV, auto-update mobile_sender.html  
✅ **Party Details** - Fill out form OR upload Canva image  
✅ **Auto GitHub Push** - Automatically deploys to your website  
✅ **Easy to Use** - Beautiful GUI, no coding required  

---

## Getting Started

### First Time Setup

1. **Install Dependencies** (if not already done):
   ```powershell
   pip install -r requirements.txt
   ```

2. **Launch the App**:
   - Double-click `Start_Party_Manager.bat`
   - OR run: `pythonw party_manager.pyw`

---

## Using the App

### Tab 1: Guest List Manager

**Step 1: Upload CSV**
1. Click "📁 Upload CSV File"
2. Select your `guests.csv` file
3. Preview shows all guests

**Step 2: Update mobile_sender.html**
1. Click "✅ Update mobile_sender.html"
2. Guest data is automatically injected into the file

**Step 3: Save (Optional)**
1. Click "💾 Save To..."
2. Choose where to save the updated file
3. Transfer to your phone via email/Dropbox

---

### Tab 2: Party Details

**Option A: Fill Out Form**
1. Select "📝 Fill out form manually"
2. Enter:
   - Event Name (e.g., "Birthday Bash")
   - Date (e.g., "Saturday, Feb 14th")
   - Time (e.g., "7:00 PM")
   - Location (e.g., "The Martin's House")

**Option B: Upload Canva Image**
1. Select "🖼️ Upload event image"
2. Click "Upload Event Image"
3. Choose your Canva flyer/poster
4. Image will be displayed on the RSVP page

**Push to GitHub**
1. Click "🚀 Update & Push to GitHub"
2. App automatically:
   - Updates `index.html`
   - Commits changes to Git
   - Pushes to GitHub
3. Website updates in ~2 minutes!

---

## Tips & Tricks

### CSV Format
Your `guests.csv` should look like this:
```
Name,Phone
John Smith,5551234567
Jane Doe,5559876543
```

### Canva Images
- **Recommended Size**: 1200px wide
- **Format**: PNG or JPG
- **Content**: Include event name, date, time, location

### Before Each Party
1. Update your CSV with new guest list
2. Update Tab 1 (Guest List)
3. Update Tab 2 (Party Details)
4. Click "Push to GitHub"
5. Done! 🎊

### Troubleshooting

**"Git operation failed"**
- Make sure you're in the correct project directory
- Ensure Git is configured with your GitHub credentials
- Try pulling latest changes first: `git pull origin main`

**"File not found"**
- Make sure you're running the app from the `party-invite-app` directory
- Check that `index.html` and `mobile_sender.html` exist

**Changes not showing on website**
- Wait 2-3 minutes for GitHub Pages to redeploy
- Hard refresh your browser: `Ctrl + Shift + R`

---

## Workflow for Each New Party

1. ✅ Create new guest list CSV
2. ✅ Open Party Manager
3. ✅ Tab 1: Upload CSV → Update → Save
4. ✅ Tab 2: Enter details OR upload image
5. ✅ Click "Push to GitHub"
6. ✅ Transfer mobile_sender.html to phone
7. ✅ Send invites!

---

## Questions?

The Party Manager saves you time by automating:
- Manual HTML editing
- Git commands
- File transfers

Everything is now just a few clicks away! 🚀
