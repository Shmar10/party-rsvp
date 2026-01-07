# 🎉 Party Invite System - v2.0 User Guide

Welcome to the future of party planning! This system makes it easy to send beautiful invites and track RSVPs without any coding.

## 🚀 The Big Picture

1. **Party Manager (Tab 1 & 2)**: You use this Windows app to design your invite and manage your guest list.
2. **RSVP Website**: Guests visit your link (GitHub Pages) to say they are coming.
3. **Cloud Database (Tab 3)**: Responses are stored in Supabase, which you can view and import back into the app.
4. **Mobile Sender**: A small file you open on your phone to send the actual texts.

---

## 🛠️ Components of the System

### 1. Party Manager App
This is your "Dashboard."
- **📋 Guest List**: Where you upload your CSV or add names manually.
- **🎊 Party Details**: Where you set the date/time and choose your flyer image.
- **☁️ Cloud RSVPs**: Where you see who has replied from the web.

### 2. Your RSVP Website
Every guest gets a link like: `https://shmar10.github.io/party-rsvp`
- It works on any phone or computer.
- It can show a simple text invite or a beautiful graphic flyer.
- Guests can even add the party to their digital calendar with one tap!

### 3. mobile_sender.html
This is the magic file that lives on your phone.
- It shows your guest list with large **"Send Message"** buttons.
- When you tap a button, it opens your phone's messaging app with the invite text already typed out!

---

## 📋 Standard Workflow

### Phase 1: Setup (The App)
1. Open **Party Manager v2.0**.
2. Go to **Tab 2 (Party Details)** and fill in your event info. Click **"Push to GitHub"**.
3. Go to **Tab 1 (Guest List Manager)** and upload your `guests.csv`.

### Phase 2: Send Invites (The Phone)
1. In the app (Tab 1), click **"Update mobile_sender.html"** (Step 3).
2. Click **"Save To..."** (Step 4) and save it to a cloud folder (Dropbox/Google Drive).
3. Open that cloud folder on your phone and tap the file.
4. Tap **"Send Message"** for each guest!

### Phase 3: Track & Remind (The Cloud)
1. After a few days, open **Tab 3 (Cloud RSVPs)**.
2. Click **"Refresh Events"** and **"Load Guests"** to see who is coming.
3. Click the **"Import"** button to move the "Yes" guests back to Tab 1.
4. Use Tab 1 to send them a reminder text or "Gate Code" update!

---

## 🆘 Troubleshooting & Help

- **Indentation/Formatting**: If the app looks "squished," try resizing the window!
- **Data Not Showing**: Ensure your Supabase RLS policies are set to "Enable Read Access" (see `EMAIL_CONFIRMATIONS.md` for details).
- **Time Delay**: After pushing to GitHub, wait 90 seconds before checking your live website.

For detailed Step-by-Step setup of individual features, see:
- [PARTY_MANAGER_GUIDE.md](file:///c:/Users/shama/party-invite-app/docs/PARTY_MANAGER_GUIDE.md)
- [MULTI_EVENT_GUIDE.md](file:///c:/Users/shama/party-invite-app/docs/MULTI_EVENT_GUIDE.md)
- [ADD_TO_CALENDAR_GUIDE.md](file:///c:/Users/shama/party-invite-app/docs/ADD_TO_CALENDAR_GUIDE.md)

**Happy Planning!** 🎉🎈
