(() => {
  const cfg = window.SUPABASE_CONFIG || {};
  if (!cfg.url || !cfg.anonKey) {
    console.error("Supabase config missing. Copy frontend/js/config.example.js to frontend/js/config.js and set credentials.");
  }
  window.supabaseClient = window.supabase.createClient(cfg.url, cfg.anonKey, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true
    }
  });
})();


