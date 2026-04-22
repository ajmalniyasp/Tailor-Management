
(function(){
  // Theme: load preference
  const stored = localStorage.getItem('theme') || 'light';
  if (stored === 'dark') document.documentElement.classList.add('dark');

  // Attach toggler if present
  const toggle = document.getElementById('themeToggle');
  if (toggle){
    toggle.addEventListener('click', function(){
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      toggle.innerText = isDark ? 'Light' : 'Dark';
    });
    // set label
    toggle.innerText = document.documentElement.classList.contains('dark') ? 'Light' : 'Dark';
  }

  // Fake session helpers
  window.auth = {
    getSession(){
      try { return JSON.parse(localStorage.getItem('ems_session') || '{}'); }
      catch(e){ return {}; }
    },
    setSession(sess){
      localStorage.setItem('ems_session', JSON.stringify(sess));
    },
    clearSession(){
      localStorage.removeItem('ems_session');
    },
    logout(){
      this.clearSession();
      window.location.href = 'signin.html';
    }
  };

  // Bind logout if available
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn){
    logoutBtn.addEventListener('click', function(e){
      e.preventDefault();
      auth.logout();
    });
  }
})();
