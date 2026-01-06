# 🔧 Quick Setup - Add "Attending" Column to Supabase

## You Need to Add One Column to Your Database

1. Go to your Supabase project: https://yupowktiegsjzcymqhkw.supabase.co
2. Click **Table Editor** → **`rsvps`** table
3. Click the **"+"** button (Add Column)
4. Fill in:
   - **Name**: `attending`
   - **Type**: `text`
   - **Default Value**: Leave blank
   - **Is Nullable**: ✅ Check this box
5. Click **Save**

## That's It!

Your RSVP form will now save whether people are attending or not! 🎉

The form has been updated to:
- ✅ Ask "Will you be attending?" with Yes/No options
- ✅ Redirect to a custom thank you page
- ✅ Show different messages for Yes vs No responses
- ✅ Prevent duplicate submissions (basic check)
