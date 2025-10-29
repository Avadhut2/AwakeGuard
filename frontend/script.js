import { createClient } from 'https://esm.sh/@supabase/supabase-js'

// ----------------------
// Supabase Setup
// ----------------------
const supabaseUrl = "https://upevjliguncwatxuwdfi.supabase.co"
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVwZXZqbGlndW5jd2F0eHV3ZGZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwNTU2NzksImV4cCI6MjA3MjYzMTY3OX0.m2yV0CUX-gnQc3RUrevkkpTvCMZf_DBnUamf6FeX1Yk" // Replace with your anon/public key
const supabase = createClient(supabaseUrl, supabaseKey)

const container = document.getElementById('alert-container')

// ----------------------
// Load initial alerts
// ----------------------
async function loadInitialAlerts() {
  const { data, error } = await supabase
    .from('alerts')
    .select('*')
    .order('timestamp', { ascending: false })
    .limit(10)

  console.log('Initial alerts:', data, error)  // Debugging

  container.innerHTML = ''
  if (data && data.length > 0) {
    data.forEach(addAlertToDashboard)
  } else {
    container.innerHTML = '<div class="loading">No alerts found.</div>'
  }
}

// ----------------------
// Add alert to dashboard
// ----------------------
function addAlertToDashboard(alert) {
  const card = document.createElement('div')
  card.className = 'alert-card new-alert'

  card.innerHTML = `
    
    <div class="alert-details">
      <strong>Driver ID: ${alert.driver_id || 'Unknown'}</strong><br>
      <span class="alert-time">🕒 ${new Date(alert.timestamp).toLocaleString()}</span><br>
      <span class="alert-location">📍 ${alert.location || 'Unknown'}</span><br>
      <span>Status: ${alert.status || 'Drowsy Detected'}</span>
    </div>
  `
  container.prepend(card)

  // Remove flash effect after 1 second
  setTimeout(() => card.classList.remove('new-alert'), 1000)
}

// ----------------------
// Real-time updates
// ----------------------
supabase.channel('realtime-alerts')
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'alerts' }, payload => {
    console.log('New alert received:', payload.new)
    addAlertToDashboard(payload.new)
  })
  .subscribe()

// ----------------------
// Initialize
// ----------------------
loadInitialAlerts()
