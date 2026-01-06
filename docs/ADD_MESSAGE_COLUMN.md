# Adding the Message Column to Supabase

To support the new "Message to Host(s)" field in your RSVP form, you need to add a `message` column to your `rsvps` table in Supabase.

## Instructions

1.  Log in to your [Supabase Dashboard](https://app.supabase.com/).
2.  Select your project.
3.  Click on **Table Editor** in the left sidebar.
4.  Select the `rsvps` table.
5.  Click the **+** button (or **Add column**) in the table header.
6.  Configure the new column:
    *   **Name**: `message`
    *   **Type**: `text`
    *   **Is Nullable**: Checked (guests may choose not to leave a message)
7.  Click **Save**.

That's it! Your RSVP form is now ready to capture and store messages from your guests.
