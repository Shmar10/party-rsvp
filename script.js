// Supabase Configuration
const SUPABASE_URL = 'https://yupowktiegsjzcymqhkw.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1cG93a3RpZWdzanpjeW1xaGt3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc2MjA3NTAsImV4cCI6MjA4MzE5Njc1MH0.AiqEpxjmMc3rczfzHx8b-omVAwJUhflIL849nNTqDwQ';

// Initialize Supabase client (renamed to avoid browser extension conflicts)
const supabaseClient = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;

// DOM Elements
const rsvpForm = document.getElementById('rsvpForm');
const submitBtn = document.getElementById('submitBtn');
const messageEl = document.getElementById('message');

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

    if (!supabaseClient) {
        showMessage('Supabase failed to initialize. Please check your configuration.', 'error');
        return;
    }

    // Toggle loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    messageEl.classList.add('hidden');

    const formData = new FormData(rsvpForm);
    const rsvpData = {
        guest_name: formData.get('name'),
        party_size: parseInt(formData.get('guests')),
        notes: formData.get('dietary')
    };

    try {
        const { data, error } = await supabaseClient
            .from('rsvps')
            .insert([rsvpData]);

        if (error) throw error;

        showMessage('Thanks for the RSVP! We can\'t wait to see you there.', 'success');
        rsvpForm.reset();
    } catch (err) {
        console.error('Error submitting RSVP:', err);
        showMessage('Oops! Something went wrong. Please try again.', 'error');
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
});
