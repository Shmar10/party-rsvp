# 📅 Add to Calendar Feature - How It Works

## What It Does

When guests RSVP "Yes" to your party, they see a "📅 Add to Calendar" button on the thank you page. Clicking it downloads a `.ics` file that works across ALL platforms!

---

## ✅ Universal Compatibility

The `.ics` (iCalendar) format works on:

- ✅ **iPhone/iPad** - Apple Calendar
- ✅ **Android** - Google Calendar
- ✅ **Windows** - Outlook
- ✅ **Mac** - Calendar.app
- ✅ **Any calendar app** that supports iCalendar standard

---

## How It Works

### For Guests:

1. Submit RSVP saying "Yes, I'll be there!"
2. See thank you page with event details
3. Click "📅 Add to Calendar" button
4. File downloads (event.ics)
5. Phone/computer recognizes it and asks to add to calendar
6. Done! Event is in their calendar 🎉

### What Gets Added:

- **Event Name** - From Party Manager
- **Date & Time** - Automatically parsed
- **Location** - Where your party is
- **Duration** - Assumes 3 hours (can be changed)
- **Description** - Event title + "See you there!"

---

## Technical Details

### Date/Time Parsing

The system automatically parses common date formats:
- "Saturday, Jan 24th" → January 24
- "6:00 PM start" → 6:00 PM
- "7:30 PM" → 7:30 PM

**Supported formats:**
- Month names: Jan, Feb, Mar, etc.
- Time: "6:00 PM", "6 PM", "18:00"

### Event Duration

Default: 3 hours from start time

To change this, edit `thank-you.html`:
```javascript
const endDate = new Date(startDate.getTime() + (3 * 60 * 60 * 1000)); // Change 3 to desired hours
```

---

## Automatic Integration

The Party Manager automatically:
1. Embeds event details in your RSVP page
2. Passes them to the thank you page
3. Generates the .ics file with correct information

**You don't need to do anything!** Just use Party Manager as normal.

---

## How to Test

1. Go to your RSVP page
2. Fill out form and select "Yes"
3. Submit
4. Click "Add to Calendar" on thank you page
5. Check that the .ics file downloads
6. Open it - your calendar app should pop up!

---

## Browser Compatibility

Works in all modern browsers:
- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Mobile browsers ✅

---

## Benefits for Your Guests

⏰ **Never forget** - Event is in their calendar  
🔔 **Reminders** - Their calendar app can remind them  
📱 **Everywhere** - Syncs across all their devices  
✨ **One click** - Super easy to use  

---

## FAQ

**Q: Will it work on old phones?**  
A: Yes! The .ics format has been standard since 1998.

**Q: Can guests edit the calendar entry?**  
A: Yes, once it's in their calendar, they can modify it (add notes, change reminders, etc.)

**Q: What if the date format is different?**  
A: The parser handles most common formats. If you use an unusual format, the event might default to current year - let me know and I can enhance the parser!

**Q: Can I change the event duration?**  
A: Yes! Edit the `thank-you.html` file and change the hours value.

---

Your guests will love this feature! 🎊
