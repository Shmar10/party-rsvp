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

To push your code changes to Supabase, you first need the **Supabase CLI** installed on your computer. Run these commands in your terminal (VS Code Terminal or PowerShell) from the `party-invite-app` folder:

0.  **Install Supabase CLI** (if you haven't yet):
    - Run: `npm install -g supabase`
    - *Note: If this gives an error, you can just add `npx` before the other commands below.*

1.  **Link your project**:
    - Run: `supabase link --project-ref YOUR_PROJECT_ID`
    - *Note: You can find your Project ID in your Supabase dashboard URL or under Project Settings > General.*
2.  **Set your API Key** (if you haven't yet):
    - Run: `supabase secrets set RESEND_API_KEY=re_gq3QBzW7_DPB1voJR4X2...`
    - *Note: Use the full key from your `docs/resend_key` file.*
3.  **Deploy**:
    - Run: `supabase functions deploy send-rsvp-confirmation`

Once deployed, any new RSVP will trigger this updated function!
