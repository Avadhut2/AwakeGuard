document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const errorEl = document.getElementById('error-message');
  const btn = document.getElementById('login-btn');

  // If already logged in, go to dashboard
  window.supabaseClient.auth.getSession().then(({ data }) => {
    if (data && data.session) {
      window.location.href = './dashboard.html';
    }
  });

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorEl.classList.add('hidden');
    errorEl.textContent = '';
    btn.disabled = true;
    btn.textContent = 'Signing in...';

    const email = /** @type {HTMLInputElement} */(document.getElementById('email')).value.trim();
    const password = /** @type {HTMLInputElement} */(document.getElementById('password')).value;

    const { error } = await window.supabaseClient.auth.signInWithPassword({ email, password });
    if (error) {
      errorEl.textContent = error.message || 'Login failed';
      errorEl.classList.remove('hidden');
      btn.disabled = false;
      btn.textContent = 'Sign In';
      return;
    }

    window.location.href = './dashboard.html';
  });
});


