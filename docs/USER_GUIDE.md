# 🎉 Party Invite System - Complete User Guide

## Overview

This system helps you send party invitations via text message and collect RSVPs through a beautiful web form. Here's what you can do:

- **Send invites** from your Android phone with pre-filled messages
- **Collect RSVPs** through a custom web page
- **Track responses** in your Supabase database

---

## 📋 What You Need

- ✅ Android phone (for sending invites)
- ✅ Computer (for initial setup)
- ✅ GitHub account (free)
- ✅ Supabase account (free)
- ✅ Guest list with names and phone numbers

---

## Part 1: Setting Up Your RSVP Website

### Step 1: Create Supabase Database

1. Go to [supabase.com](https://supabase.com) and sign up
2. Click **"New Project"**
3. Enter project details and click **"Create new project"** (wait ~2 minutes)
4. Go to **Table Editor** → **"Create a new table"**
5. Name it `rsvps` and add these columns:
   - `id` (already there)
   - `name` (type: text)
   - `guests` (type: int4)
   - `dietary_notes` (type: text)
   - `created_at` (type: timestamptz, default: now())
6. Click **"Save"**

### Step 2: Get Your Credentials

1. Go to **Project Settings** (gear icon) → **API**
2. Copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public key** (long string)
3. Keep these safe - you'll need them!

### Step 3: Deploy to GitHub Pages

**Your RSVP website is already live at:**
**https://shmar10.github.io/party-rsvp** ✅

To verify it's working:
1. Visit the URL
2. Fill out a test RSVP
3. Check Supabase **Table Editor** → `rsvps` table
4. You should see your test entry!

---

## Part 2: Preparing to Send Invites

### Step 1: Create Your Guest List

1. Open `guests.csv` on your computer
2. Format it like this:
   ```
   Name,Phone
   John Smith,5551234567
   Jane Doe,5559876543
   ```
3. Save the file

### Step 2: Edit mobile_sender.html

1. Right-click `mobile_sender.html` → **Open with Notepad**
2. Find the section marked `// Add your guests here`
3. Replace with your guest data:
   ```javascript
   const guests = [
       { name: "John Smith", phone: "5551234567" },
       { name: "Jane Doe", phone: "5559876543" },
       // Add more guests...
   ];
   ```
4. **Save the file**

### Step 3: Transfer to Your Phone

**Option A: Email Method**
1. Email `mobile_sender.html` to yourself
2. Open email on your phone
3. Download the attachment

**Option B: Cloud Storage**
1. Upload `mobile_sender.html` to Google Drive/Dropbox
2. Open Drive/Dropbox on your phone
3. Download the file

---

## Part 3: Sending Invites from Your Phone

### Step 1: Open the App

1. On your Android phone, locate `mobile_sender.html`
2. Open it with **Chrome** or your browser
3. You'll see a beautiful purple page with all your guests!

### Step 2: Send Messages

For each guest:

1. **Tap "Send Message"** button
2. Your **Messages app opens** with pre-filled text:
   ```
   Hey [Name]! Hope you can make it. RSVP here: https://shmar10.github.io/party-rsvp
   ```
3. **Tap "Send"** in Messages
4. **Go back** to the web page
5. The guest is marked as "✓ Sent"
6. Repeat for next guest!

### Tips:
- The page **tracks who you've sent to** (uses browser storage)
- You can close and reopen - it remembers!
- **Long-press the header** for 2 seconds to reset all statuses

---

## Part 4: Tracking RSVPs

### View Responses in Supabase

1. Go to your Supabase project
2. Click **Table Editor** → `rsvps`
3. You'll see all responses with:
   - Guest name
   - Number of guests
   - Dietary notes
   - Timestamp

### Export Guest List

1. In Supabase Table Editor, click the **"..."** menu
2. Select **"Export to CSV"**
3. Use this for planning (catering, seating, etc.)

---

## 📱 Quick Reference Card

### Sending Invites:
1. Open `mobile_sender.html` on phone
2. Tap "Send Message" for each guest
3. Tap "Send" in Messages app
4. Return to web page
5. Repeat!

### Checking RSVPs:
1. Open Supabase
2. Table Editor → `rsvps`
3. View all responses

### Your Links:
- **RSVP Page**: https://shmar10.github.io/party-rsvp
- **Supabase**: https://yupowktiegsjzcymqhkw.supabase.co

---

## 🆘 Troubleshooting

### "Could not load guests"
- Make sure you edited the `guests` array in `mobile_sender.html`
- Check that the format matches the example exactly

### RSVP form not saving
- Verify Supabase credentials in `script.js` are correct
- Check that the `rsvps` table exists in Supabase

### Messages not opening on phone
- Make sure you're using Chrome or a modern browser
- The phone number format should be digits only (no dashes)

### Need to reset sent status?
- Long-press the header in `mobile_sender.html` for 2 seconds
- Confirm reset

---

## 🎊 You're All Set!

Your party invite system is ready to go. Just:

1. ✅ Edit `mobile_sender.html` with your guests
2. ✅ Transfer to your phone
3. ✅ Start sending invites!
4. ✅ Watch RSVPs roll in at your Supabase dashboard

**Have an amazing party!** 🎉
