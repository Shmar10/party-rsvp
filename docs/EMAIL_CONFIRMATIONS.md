# Adding Email Confirmations

To enable email confirmations for your guests, follow these two steps.

## Step 1: Update your Supabase Table

You need to add a new column to your `rsvps` table to store the email addresses.

1.  Go to your **Supabase Dashboard**.
2.  Open your project and go to the **Table Editor**.
3.  Select the `rsvps` table.
4.  Click **Insert** -> **Column** (or use the `+` button on the far right).
5.  Name the column: `email` (Type: `text`)
6.  Name the column: `event_date` (Type: `text`)
7.  Name the column: `event_time` (Type: `text`)
8.  Name the column: `event_location` (Type: `text`)
9.  Default Value: `NULL` for all (uncheck "Is Required").
10. Save the changes.

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

### Redeploying the Function
If you have already deployed this function, you must redeploy it for the changes to take effect:

1.  Open your terminal in the project directory.
2.  Run: `supabase functions deploy send-rsvp-confirmation`
