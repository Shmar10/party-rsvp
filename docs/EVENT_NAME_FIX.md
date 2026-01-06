# Event Name Field - Now Always Visible

## Issue
When uploading an image instead of filling in the form, the Event Name field was hidden. This meant:
- No event name was captured for multi-event tracking
- RSVPs couldn't be filtered by event
- Event history didn't save properly

## Solution ✅

**Event Name field is now ALWAYS visible, regardless of form or image mode!**

### What Changed:

1. **Moved Event Name Field**
   - Now appears above the "Choose how to set up your party" section
   - Always visible whether you choose "Fill out form" or "Upload image"
   - Has clear label: "Event Name (Required for Tracking)"

2. **Added Visual Separator**
   - Horizontal line separates event name from mode choice
   - Clearer UI hierarchy

3. **Added Tooltip**
   - Hover over Event Name field: "This name is used to track RSVPs for your event"

4. **Both Modes Use Event Name**
   - **Form mode**: Uses event name + all form fields
   - **Image mode**: Uses event name + uploaded image
   - Both update `data-event-name` attribute correctly

### Workflow Now:

**Image Mode:**
1. Enter Event Name (e.g., "Pool Party 2026")
2. Select "Upload event image"
3. Click "Upload Event Image" button
4. Choose your Canva image
5. Click "Push to GitHub"
6. ✅ Event tracked with proper name!

**Form Mode:**
1. Enter Event Name
2. Select "Fill out form manually"  
3. Fill in description, date, time, location
4. Click "Push to GitHub"
5. ✅ Event tracked with proper name!

## Benefits

✅ Multi-event tracking works in both modes  
✅ Event history saves correctly  
✅ RSVPs can be filtered by event name  
✅ Clearer what's required vs optional  
✅ No confusion about what to fill in

Try it out! The Event Name field is now prominent and always visible. 🎉
