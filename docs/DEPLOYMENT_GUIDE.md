# GitHub Pages Deployment Guide

## Files to Upload to Your Repository

Upload these files to https://github.com/Shmar10/party-rsvp:

### Required Files (for RSVP website):
1. `index.html` - Main RSVP form page
2. `script.js` - Supabase integration (already configured!)
3. `styles.css` - Styling for the RSVP page

### Optional (for reference):
- `README.md` - Project documentation
- `mobile_sender.html` - For sending invites from your phone (don't need to upload this)

## Step-by-Step Upload Instructions

### Option A: Upload Files Directly via GitHub Website

1. Go to https://github.com/Shmar10/party-rsvp
2. Click the **"Add file"** button → **"Upload files"**
3. Drag and drop these files:
   - `index.html`
   - `script.js`
   - `styles.css`
4. Scroll down and click **"Commit changes"**

### Option B: Use GitHub Desktop (Easier for Multiple Files)

1. Download GitHub Desktop: https://desktop.github.com
2. Sign in with your GitHub account
3. Clone your repository
4. Copy the 3 files into the cloned folder
5. Commit and push

## Enable GitHub Pages

1. Go to your repository: https://github.com/Shmar10/party-rsvp
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under **Source**, select:
   - **Branch**: `main` (or `master`)
   - **Folder**: `/ (root)`
5. Click **Save**
6. Wait ~2 minutes for deployment

## Your Website Will Be Live At:
**https://shmar10.github.io/party-rsvp**

## Testing Your RSVP Page

1. Visit https://shmar10.github.io/party-rsvp
2. Fill out the form
3. Submit
4. Check Supabase dashboard → Table Editor → `rsvps` table
5. You should see your test entry!

## Next Steps

1. ✅ Upload files to GitHub
2. ✅ Enable GitHub Pages
3. ✅ Test the RSVP form
4. ✅ Edit `mobile_sender.html` on your phone with your guest list
5. ✅ Start sending invites! 🎉

The link in `mobile_sender.html` is already set to: https://shmar10.github.io/party-rsvp
