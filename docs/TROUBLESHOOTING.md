# 🔍 Troubleshooting Steps - RSVP Not Saving

## About Those Buttons You Circled:

### 🔒 "RLS disabled" 
**What it is:** Row Level Security - Controls who can read/write data in your table.

**Current Status:** DISABLED ⚠️
- **Good news:** Anyone can submit RSVPs (which is what you want)
- **Bad news:** Anyone can also DELETE or modify RSVPs (security risk)

**Should you worry?** 
- For a small private party with trusted guests: **Low risk**
- For a public event: **Enable RLS with policies**

**How to secure it later (optional):**
1. Click "RLS disabled" → Enable RLS
2. Create a policy that allows INSERT for anonymous users
3. Create a policy that allows SELECT/UPDATE/DELETE only for authenticated users (you)

### 🔄 "Enable Realtime"
**What it is:** Live updates when data changes in the table.

**Do you need it?** **NO** - Not necessary for an RSVP form. It's for apps that need instant notifications when database changes.

---

## Why RSVPs Might Not Be Saving:

### Issue 1: Browser Cache
GitHub Pages may have updated but your browser is showing old code.

**Fix:**
1. Open https://shmar10.github.io/party-rsvp
2. Press `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac) to hard refresh
3. Try submitting again

### Issue 2: Check Browser Console for Errors

**How to check:**
1. On your RSVP page, press `F12` to open Developer Tools
2. Click the **"Console"** tab
3. Try submitting the form
4. Look for any **red error messages**
5. **Screenshot and share them with me**

### Issue 3: Verify GitHub Pages Updated

Check if the fix deployed:
1. Go to https://shmar10.github.io/party-rsvp
2. Right-click anywhere → "View Page Source"
3. Search for `guest_name` (Ctrl+F)
4. If you see `name:` instead of `guest_name:`, the update hasn't deployed yet

---

## Quick Test with Console

Try this to test if Supabase connection works:

1. Open https://shmar10.github.io/party-rsvp
2. Press `F12` → **Console** tab
3. Paste this code and press Enter:

```javascript
supabase.from('rsvps').insert([
  { guest_name: 'Console Test', party_size: 1, notes: 'Testing from console' }
]).then(result => console.log('Result:', result));
```

4. If you see "Result: {data: null, error: null}" - **It works!**
5. If you see an error - **Screenshot it for me**

---

## Next Steps:

1. ✅ Hard refresh the page (Ctrl+Shift+R)
2. ✅ Check browser console for errors
3. ✅ Try the console test above
4. ✅ Share screenshots of any errors you see

Let me know what you find!
