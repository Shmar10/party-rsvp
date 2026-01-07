// 1. IMPORTS
// We import the Supabase client (standard) and the Resend library for emails.
import { createClient } from 'jsr:@supabase/supabase-js@2'
import { Resend } from 'npm:resend'

// 2. INITIALIZE RESEND
// This grabs the API key you saved earlier using 'supabase secrets set'
const resend = new Resend(Deno.env.get('RESEND_API_KEY'))

// 3. THE MAIN FUNCTION
// This listens for incoming webhooks from your database.
Deno.serve(async (req) => {
  
  // Security Check: Ensure this is a POST request (standard for webhooks)
  if (req.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 })
  }

  try {
    // 4. PARSE DATA
    // 'payload' contains the data sent by the database trigger
    const payload = await req.json()
    const record = payload.record // The actual row data (email, attending, etc.)

    // Safety Check: specific columns must exist
    if (!record.email || !record.attending) {
      console.log('Skipping: Missing email or attending status')
      return new Response('Skipped: Missing data', { status: 200 })
    }

    // 5. PREPARE EMAIL CONTENT
    const isAttending = record.attending.toLowerCase().trim() === 'yes'
    const eventName = record.event_name || 'the party'
    const eventDate = record.event_date || 'TBD'
    const eventTime = record.event_time || 'TBD'
    const eventLocation = record.event_location || 'TBD'
    
    let subject = ''
    let htmlContent = ''

    if (isAttending) {
      subject = `Confirmation: You're going to ${eventName}!`
      htmlContent = `
        <div style="font-family: sans-serif; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
          <h2 style="color: #667eea;">We can't wait to see you!</h2>
          <p>Hi ${record.guest_name || 'there'},</p>
          <p>This email confirms your RSVP for <strong>${eventName}</strong>.</p>
          
          <div style="background: #f7f7ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p style="margin: 5px 0;"><strong>📅 Date:</strong> ${eventDate}</p>
            <p style="margin: 5px 0;"><strong>⏰ Time:</strong> ${eventTime}</p>
            <p style="margin: 5px 0;"><strong>📍 Location:</strong> ${eventLocation}</p>
          </div>

          <p>If you need to change your plans, please contact the host.</p>
          <br />
          <p>Cheers!</p>
        </div>
      `
    } else {
      subject = `We will miss you at ${eventName}`
      htmlContent = `
        <div style="font-family: sans-serif; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
          <h2 style="color: #ed4245;">We'll miss you.</h2>
          <p>Hi ${record.guest_name || 'there'},</p>
          <p>We received your RSVP that you cannot make it to <strong>${eventName}</strong>.</p>
          <p>We're sorry you can't join us this time, but we hope to catch up at the next celebration!</p>
          <br />
          <p>Best regards,</p>
        </div>
      `
    }

    // 6. SEND THE EMAIL
    // FROM: Must use your verified domain (rsvp@shmarten.com)
    // TO: The guest's email from the database record
    const data = await resend.emails.send({
      from: 'RSVP <rsvp@shmarten.com>', 
      to: record.email,
      subject: subject,
      html: htmlContent,
    })

    console.log(`Email sent to ${record.email}:`, data)

    // 7. RETURN SUCCESS
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
      status: 200,
    })

  } catch (error) {
    // Error Handling: If something breaks, log it so you can see it in Supabase logs
    console.error('Error sending email:', error)
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { 'Content-Type': 'application/json' },
      status: 500,
    })
  }
})