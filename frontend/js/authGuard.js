document.addEventListener('DOMContentLoaded', async () => {
  const { data } = await window.supabaseClient.auth.getSession();
  if (!data || !data.session) {
    window.location.href = './index.html';
    return;
  }

  const emailEl = document.getElementById('user-email');
  if (emailEl) {
    emailEl.textContent = data.session.user.email || '';
  }

  document.getElementById('logout-btn')?.addEventListener('click', async () => {
    await window.supabaseClient.auth.signOut();
    window.location.href = './index.html';
  });
});


