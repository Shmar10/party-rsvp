# v2.0 Stability Plan

## Issues to Fix

1. **Git Push Hanging** ❌ Critical
2. **Drag-Drop Not Working** ⚠️ Non-critical  
3. **Calendar Widget Issues** ⚠️ Medium

## Solution: Create Stable v2.0

### Keep (Working):
- ✅ Tooltips on all buttons
- ✅ Event Name always visible
- ✅ Recent events dropdown
- ✅ Enhanced status bar with timestamps
- ✅ Better button layout

### Remove (Problematic):
- ❌ Drag-and-drop CSV (tkinterdnd2 compatibility)
- ❌ Threaded Git push (causing hangs)
- ❌ Progress bar dialog (part of threading issue)

### Simplify:
- Use standard Entry for date instead of DateEntry
- Synchronous Git operations (like v1)
- Simple status updates instead of progress dialog

## Implementation
Creating `party_manager_v2_stable.pyw` with reliable features only.
