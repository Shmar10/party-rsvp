# Party Manager v2.0 - Complete Feature List

## All New Features Implemented

### 1. Tooltips Everywhere ✅
**Hover over any button or field to see helpful hints!**

- Guest List tab:
  - Upload CSV button: "Select your guests.csv file with Name and Phone columns"
  - Update button: "Inject guest list into mobile_sender.html for sending"
  - Save button: "Save updated mobile_sender.html to a location of your choice"

- Party Details tab:
  - Recent Events dropdown: "Select a previous party to load all its details"
  - Upload Image button: "Select a Canva image with all event details"
  - Push to GitHub button: "Update index.html and deploy to your website (saves to history)"

### 2. Progress Bar for GitHub Operations ✅
**No more frozen windows!**

- Shows a popup dialog during deploy
- Real-time status updates:
  - "Adding files to Git..."
  - "Committing changes..."
  - "Pushing to GitHub..."
- Threaded operations - app stays responsive
- Auto-closes on success or error

### 3. Drag & Drop CSV Upload ✅
**Just drag and drop your guests.csv file!**

- Drag file from anywhere on your computer
- Drop it anywhere in the Guest List tab
- Instantly loads - no clicking needed!
- Still works with the "Upload CSV" button too
- Visible hint: "💡 Tip: Drag and drop your CSV file anywhere in this window!"

### 4. Recent Events Dropdown ✅
**Quick access to your party history!**

- Dropdown appears automatically if you have history
- Shows last 10 events
- Click to instantly load all details:
  - Event Name
  - Description
  - Date
  - Time
  - Location
- Automatically saves when you push to GitHub
- History stored in `.party_events_history.json`

## Additional Enhancements

### Status Bar Improvements
- Now shows timestamps with every action
- Example: "Loaded 15 guests | 11:59:30"
- Shows "Party Manager v2.0" in status

### Window Improvements
- Slightly larger window (950x750 vs 900x700)
- Better spacing for new features
- Updated title: "🎉 Party Manager v2.0"

## How To Use v2.0

### Launch
```
Start_Party_Manager_V2.bat
```

Or double-click: `party_manager_v2.pyw`

### Quick Workflow
1. **Drag your CSV** into the Guest List tab
2. Click "Update mobile_sender.html"
3. Switch to Party Details tab
4. **(Optional)** Load from recent events dropdown
5. Fill in or update party details
6. Click "🚀 Update & Push to GitHub"
7. Watch the progress bar!
8. Done! Event automatically saved to history

## Files Created/Modified

**New Files:**
- `party_manager_v2.pyw` - Complete v2.0 application
- `Start_Party_Manager_V2.bat` - Easy launcher
- `docs/V2_README.md` - Installation guide
- `.party_events_history.json` - Auto-created on first push

**Updated Files:**
- `requirements.txt` - Added tkinterdnd2

## Backward Compatibility

Your original `party_manager.pyw` still works! You can use either version:
- `Start_Party_Manager.bat` - Original v1
- `Start_Party_Manager_V2.bat` - New v2.0

## Known Limitations

- Drag-and-drop requires Windows 10+ (gracefully degrades if not available)
- Event history limited to last 10 parties
- Progress bar is "indeterminate" (doesn't show %)

## Tips

1. **Use Recent Events**: Save time by loading from history
2. **Hover Everything**: Tooltips explain what each button does
3. **Drag Files**: Faster than clicking "Browse"
4. **Watch Progress**: No need to wonder if it's working

Enjoy Party Manager v2.0! 🎉
