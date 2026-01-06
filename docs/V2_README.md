# Party Manager v2.0 - Installation Guide

## New Requirements

Before running v2.0, install this additional library:

```powershell
pip install tkinterdnd2
```

**If installation fails:** The app will still work, but drag-and-drop won't be available. You can still use the "Upload CSV" button.

## What's New in v2.0

### 1. Tooltips Everywhere
Hover over any button or field to see helpful descriptions.

### 2. Progress Bar for GitHub Push
No more wondering if the app froze! See real-time progress when deploying.

### 3. Drag & Drop CSV Upload
Just drag your guests.csv file into the window - no clicking needed!

### 4. Recent Events Dropdown
Quickly reload settings from previous parties. No re-typing!

## How to Run

**Use the new version:**
```
Start_Party_Manager_V2.bat
```

Or double-click: `party_manager_v2.pyw`

## Your Data

Recent events are saved in: `.party_events_history.json`
- Keeps last 10 parties
- Automatically saves when you push to GitHub
- Delete this file to clear history

Enjoy the upgraded Party Manager! 🎉
