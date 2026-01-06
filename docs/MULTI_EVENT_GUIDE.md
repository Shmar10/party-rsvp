# 🎯 Multi-Event Tracking - Setup Guide

## What This Does

Your RSVP system now tracks which event each RSVP is for! This means you can host multiple parties without mixing up the guest lists.

---

## ✅ Step 1: Add Column to Supabase (ONE TIME)

1. Go to your Supabase project: https://yupowktiegsjzcymqhkw.supabase.co
2. Click **Table Editor** → **`rsvps`** table
3. Click the **"+"** button (Add Column)
4. Fill in:
   - **Name**: `event_name`
   - **Type**: `text`  
   - **Default Value**: Leave blank
   - **Is Nullable**: ✅ Check this box
5. Click **Save**

**That's it for Supabase!** You only need to do this once.

---

## ✅ How It Works Automatically

### When You Use Party Manager:

1. Open Party Manager
2. Fill in the **Event Name** field (e.g., "Shawn's Retirement Pool Party!")
3. Click "🚀 Update & Push to GitHub"

**Behind the scenes:**
- Party Manager embeds the event name in your RSVP page
- When guests submit RSVPs, the event name is automatically included
- All RSVPs are tagged with the event they're for

---

## ✅ Viewing RSVPs by Event

### In Supabase Table Editor:

1. Go to Table Editor → `rsvps`
2. Click the **Filter** button
3. Add filter:
   - **Column**: `event_name`
   - **Operator**: `equals`
   - **Value**: Type your event name (e.g., "Shawn's Retirement Pool Party!")
4. Click Apply

You'll see only RSVPs for that specific event!

### Export by Event:

1. Apply the filter (above)
2. Click **"..."** menu → **Export to CSV**
3. You get a clean list for just that event

---

## ✅ Workflow for Each New Party

1. Open Party Manager
2. **Tab 1**: Upload new guest list → Update mobile_sender.html
3. **Tab 2**: 
   - Enter **NEW Event Name** (this is the key!)
   - Enter event details
   - Click "Update & Push to GitHub"
4. Send invites from your phone
5. **In Supabase**: Filter by the new event name to see RSVPs

---

## 💡 Pro Tips

### Keep Event Names Unique
- ❌ Bad: "Party", "Celebration" (too generic)
- ✅ Good: "Shawn's Retirement Pool Party 2026", "Sarah's Birthday Bash"

### Archive Old Events
You don't need to delete old RSVPs! They're automatically separated by event name. Keep them for future reference!

### Quick Stats
In Supabase, you can see:
- Total RSVPs per event
- Who said Yes vs No
- Dietary restrictions per event

---

## 🎉 Benefits

✅ **No More Manual Cleanup** - Keep all historical data  
✅ **Easy Filtering** - See RSVPs for any past or current event  
✅ **Better Planning** - Learn from past parties  
✅ **Automatic** - No extra work for you!

Your multi-party RSVP system is now ready! 🚀
