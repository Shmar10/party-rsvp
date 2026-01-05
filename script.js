// Supabase Configuration
const SUPABASE_URL = 'https://yupowktiegsjzcymqhkw.supabase.co';
const SUPABASE_KEY = 'sb_publishable_fYWDxGWU9ylcjmnq9hJ4xw_25H4HdRm';

// Initialize Supabase client
const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;

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

    if (!supabase) {
        showMessage('Supabase failed to initialize. Please check your configuration.', 'error');
        return;
    }

    // Toggle loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    messageEl.classList.add('hidden');

    const formData = new FormData(rsvpForm);
    const rsvpData = {
        name: formData.get('name'),
        guests: parseInt(formData.get('guests')),
        dietary_notes: formData.get('dietary')
    };

    try {
        const { data, error } = await supabase
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
