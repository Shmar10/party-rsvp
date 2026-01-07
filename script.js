// Supabase Configuration
const SUPABASE_URL = 'https://yupowktiegsjzcymqhkw.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1cG93a3RpZWdzanpjeW1xaGt3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc2MjA3NTAsImV4cCI6MjA4MzE5Njc1MH0.AiqEpxjmMc3rczfzHx8b-omVAwJUhflIL849nNTqDwQ';

// Toggle to open or close the RSVP form
const RSVP_OPEN = true;

// Initialize Supabase client
const supabaseClient = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;

// DOM Elements
const rsvpForm = document.getElementById('rsvpForm');
const submitBtn = document.getElementById('submitBtn');
const messageEl = document.getElementById('message');
const rsvpSection = document.querySelector('.rsvp-card');
const rsvpClosedMessage = document.getElementById('rsvpClosedMessage');

// Initialize view based on RSVP_OPEN status
function initRSVPView() {
    if (!RSVP_OPEN) {
        if (rsvpForm) rsvpForm.classList.add('hidden');
        if (rsvpClosedMessage) rsvpClosedMessage.classList.remove('hidden');
        const rsvpTitle = document.querySelector('.rsvp-card h2');
        if (rsvpTitle) rsvpTitle.classList.add('hidden');
    }
}

// Run on load
document.addEventListener('DOMContentLoaded', initRSVPView);

/**
 * Show feedback message to the user
 */
function showMessage(text, type) {
    messageEl.textContent = text;
    messageEl.className = type;
    messageEl.classList.remove('hidden');
}

/**
 * Handle form submission
 */
rsvpForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!RSVP_OPEN) {
        showMessage('RSVPs are currently closed.', 'error');
        return;
    }

    if (!supabaseClient) {
        showMessage('Supabase failed to initialize. Please check your configuration.', 'error');
        return;
    }

    // Toggle loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    messageEl.classList.add('hidden');

    const formData = new FormData(rsvpForm);
    const attending = formData.get('attending');
    const guestName = formData.get('name');

    // Get event name from page
    const eventName = document.querySelector('.container').getAttribute('data-event-name') || 'Unknown Event';

    // Helper to find detail text by icon emoji
    const findDetail = (emoji) => {
        const items = document.querySelectorAll('.detail-item');
        for (const item of items) {
            if (item.textContent.includes(emoji)) {
                return item.querySelector('span:last-child')?.textContent || '';
            }
        }
        return '';
    };

    const pageDate = findDetail('📅');
    const pageTime = findDetail('⏰');
    const pageLocation = findDetail('📍');

    // Check for duplicate submission (basic client-side check)
    const submittedKey = `rsvp_submitted_${guestName.toLowerCase().replace(/\s+/g, '_')}`;
    if (localStorage.getItem(submittedKey)) {
        showMessage('It looks like you already submitted an RSVP! Contact the host if you need to make changes.', 'error');
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        return;
    }

    const rsvpData = {
        guest_name: guestName,
        email: formData.get('email'),
        party_size: parseInt(formData.get('guests')),
        notes: formData.get('dietary'),
        message: formData.get('message_host'),
        attending: attending,
        event_name: eventName,
        event_date: pageDate,
        event_time: pageTime,
        event_location: pageLocation
    };

    try {
        const { data, error } = await supabaseClient
            .from('rsvps')
            .insert([rsvpData]);

        if (error) throw error;

        // Mark as submitted
        localStorage.setItem(submittedKey, 'true');

        // Redirect to thank you page with all event details for calendar
        const params = new URLSearchParams({
            attending: attending,
            event: eventName,
            date: pageDate,
            time: pageTime,
            location: pageLocation
        });
        window.location.href = `thank-you.html?${params.toString()}`;
    } catch (err) {
        console.error('Error submitting RSVP:', err);
        showMessage('Oops! Something went wrong. Please try again.', 'error');
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
});
