# 📜 Party Invite App - Development History

This document chronicles the development journey of the Party Invite Application, detailing major versions, feature additions, and critical bug fixes.

---

## 🚀 Version 3.0 (Current)
**Release Date:** January 7, 2026  
**Framework:** Flet (Python)

Version 3 represents a complete rewrite of the application using the **Flet** framework to create a modern, responsive, and more robust user interface.

### ✨ New Features
*   **Modern UI Framework**: Replaced `tkinter` with **Flet** for a sleek, dark-mode generic material design.
*   **Cloud RSVPs Integration**: 
    *   Direct connection to Supabase database.
    *   Real-time fetching of guest RSVP status.
    *   **Import to List**: One-click import of "Yes" attendees from the cloud back into your local manager for targeting.
*   **Email Broadcast System**:
    *   Integrated **Resend API** for sending email blasts.
    *   Target specific groups (e.g., "Confirmed Guests").
    *   Rich HTML email templates.
*   **Enhanced Guest Management**:
    *   Improved CSV import/export.
    *   Inline editing and deletion of guests.
    *   Real-time guest counting.

### 🛠️ Key Fixes & Refinements
*   **Flet 0.80.1 Compatibility**: 
    *   Updated deprecated `ElevatedButton` controls to modern `Button`.
    *   Fixed `NavigationBar` implementation to ensure visibility and stability.
*   **Navigation Architecture**: Implemented robust tab navigation that persists state correctly.
*   **Stability**: Fixed crashes during cloud imports and navigation switching.

---

## 🚀 Version 2.0
**Release Date:** January 6, 2026  
**Framework:** CustomTkinter (Python)

Version 2 was a major usability upgrade over the original prototype, introducing quality-of-life features and a better look and feel.

### ✨ Major Features
*   **Event Description Field**: Added support for custom subtitles/descriptions on the RSVP page.
*   **Recent Events History**: 
    *   Auto-saves event details to `.party_events_history.json`.
    *   Dropdown menu to quickly reload details from past parties.
*   **Drag & Drop Support**: Added ability to drag `guests.csv` files directly into the window.
*   **Progress Bar**: Added visual feedback for long-running operations (like GitHub pushes) to prevent the "app hung" feeling.
*   **Tooltips**: comprehensive hover tooltips on all buttons to explain functionality.
*   **Status Bar**: Added a timestamped status bar at the bottom for action feedback.

### 🐛 Bug Fixes
*   **GitHub Push Hanging**: Fixed threading issues that caused the app to freeze during deployment.
*   **Layout Fixes**: Reordered buttons in the Party Details tab for a more logical workflow (Upload Image -> Push).

---

## 🚀 Version 1.0 (Legacy)
**Release Date:** Late 2025  
**Framework:** Tkinter (Python)

The original proof-of-concept application.

### Core Capabilities
*   **Basic Guest List**: Manual entry of names and phone numbers.
*   **Mobile Sender Gen**: Generated `mobile_sender.html` for SMS invites.
*   **Simple Deployment**: Basic script to commit and push changes to GitHub.
*   **Party Details**: Basic fields for Event Name, Date, Time, and Location.

---

## 🔮 Future Roadmap
*   **Mobile App Companion**: A dedicated mobile app for check-ins at the door.
*   **QR Code Generation**: Generate check-in QR codes for guests.
*   **More Email Templates**: Additional designs for reminders, thank yous, and updates.
