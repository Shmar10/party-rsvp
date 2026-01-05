# Party RSVP App 🥂

A premium, dark-mode RSVP web application designed for elegant event invitations. This project includes a frontend website and a Python-based automation script for sending invites via Google Messages.

## 🚀 Features

- **Stunning UI**: Modern dark-mode design with glassmorphism and animated backgrounds.
- **Supabase Backend**: Simple and reliable data storage for RSVP responses.
- **Automation Robot**: Personalized SMS invite sender using Selenium and Google Messages.
- **Responsive**: Looks great on mobile and desktop.

## 🛠️ Setup Instructions

### 1. Frontend Configuration
- Open `script.js`.
- Replace `PLACEHOLDER` with your **Supabase URL** and **Publishable API Key**.
- Ensure your Supabase database has an `rsvps` table with columns: `name` (text), `guests` (int), and `dietary_notes` (text).

### 2. Automation Script Setup
- Install the required Python packages:
  ```bash
  pip install -r requirements.txt
  ```
- Open `guests.csv` and add your guest names and phone numbers.
- Update the `VERCEL_URL` variable in `send_invites.py` with your hosted website link.
- Run the script:
  ```bash
  python send_invites.py
  ```
- **Important**: You will need to scan the QR code to log into Google Messages for Web when prompted.

## 📦 Deployment
This app is ready to be hosted on **Vercel** or **Netlify**. Simply connect this repository to your hosting provider and it will deploy automatically.

---
Built with ❤️ for great parties.
