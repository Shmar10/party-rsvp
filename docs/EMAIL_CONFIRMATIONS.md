# Adding Email Confirmations

To enable email confirmations for your guests, follow these two steps.

## Step 1: Update your Supabase Table

You need to add a new column to your `rsvps` table to store the email addresses.

1.  Go to your **Supabase Dashboard**.
2.  Open your project and go to the **Table Editor**.
3.  Select the `rsvps` table.
4.  Click **Insert** -> **Column** (or use the `+` button on the far right).
5.  Name the column: `email`
6.  Type: `text`
7.  Default Value: `NULL` (uncheck "Is Required").
8.  Save the changes.

---

## Step 2: Set up the Email Automation

Since the app runs in the browser, it cannot send emails directly for security reasons. The best way to do this is using a "no-code" automation tool.

### Option A: Using Zapier (Easiest)
1.  Create a free account on [Zapier.com](https://zapier.com).
2.  Create a new **Zap**.
3.  **Trigger**: Search for **Supabase**.
    - Event: "New Row in Table".
    - Connect your DB and select the `rsvps` table.
4.  **Action**: Search for **Gmail** (or "Email by Zapier").
    - Event: "Send Email".
    - **To**: Select the `email` field from Supabase.
    - **Subject**: "RSVP Confirmed: {{event_name}}"
    - **Body**: "Hi {{guest_name}}! Thanks for RSVPing. We'll see you on {{date}}!"
5.  Turn on the Zap.

### Option B: Using Make.com
Similar to Zapier, you can use **Make.com** to watch for new records in Supabase and trigger an email through Gmail, Outlook, or Mailgun.

---

## Technical Note: Supabase Edge Functions
If you are comfortable with coding (TypeScript), you can use a **Supabase Edge Function** combined with a service like [Resend.com](https://resend.com) to send emails directly from Supabase whenever a new RSVP is added.
