// main.js — shared front-end behaviour for the SMS web app

document.addEventListener("DOMContentLoaded", () => {
  // ---- Sidebar toggle (mobile) ----
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", () => sidebar.classList.toggle("show"));
    document.addEventListener("click", (e) => {
      if (window.innerWidth < 992 && sidebar.classList.contains("show") &&
          !sidebar.contains(e.target) && e.target !== toggleBtn) {
        sidebar.classList.remove("show");
      }
    });
  }

  // ---- Auto-dismiss toasts ----
  document.querySelectorAll(".toast").forEach((toastEl) => {
    const toast = bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 4000 });
    toast.show();
  });

  // ---- Bootstrap tooltips ----
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
    new bootstrap.Tooltip(el);
  });

  // ---- Delete confirmation dialogs ----
  document.querySelectorAll("form.confirm-delete").forEach((form) => {
    form.addEventListener("submit", (e) => {
      const label = form.dataset.confirmLabel || "this record";
      if (!window.confirm(`Are you sure you want to delete ${label}? This cannot be undone.`)) {
        e.preventDefault();
      }
    });
  });

  // ---- Global loading spinner on normal navigations/form submits ----
  const spinner = document.getElementById("globalSpinner");
  const showSpinner = () => spinner && spinner.classList.remove("d-none");
  document.querySelectorAll("form:not(.no-spinner)").forEach((form) => {
    form.addEventListener("submit", () => {
      if (form.checkValidity ? form.checkValidity() : true) showSpinner();
    });
  });
  document.querySelectorAll("a.nav-link, a.page-link").forEach((link) => {
    link.addEventListener("click", () => showSpinner());
  });

  // ---- Live search typeahead (students list page) ----
  const liveInput = document.getElementById("liveSearchInput");
  const liveResults = document.getElementById("liveSearchResults");
  if (liveInput && liveResults) {
    let debounceTimer;
    liveInput.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      const q = liveInput.value.trim();
      if (!q) { liveResults.innerHTML = ""; liveResults.classList.add("d-none"); return; }

      debounceTimer = setTimeout(async () => {
        try {
          const res = await fetch(`/students/search-live?q=${encodeURIComponent(q)}`);
          const data = await res.json();
          if (!data.length) {
            liveResults.innerHTML = '<div class="list-group-item text-muted small">No matches found.</div>';
          } else {
            liveResults.innerHTML = data.map((s) => `
              <a href="/students/${s.id}" class="list-group-item list-group-item-action d-flex justify-content-between">
                <span><strong>${s.name}</strong> <span class="text-muted small">— ${s.department}</span></span>
                <span class="text-muted small">${s.email}</span>
              </a>`).join("");
          }
          liveResults.classList.remove("d-none");
        } catch (err) {
          liveResults.classList.add("d-none");
        }
      }, 250);
    });

    document.addEventListener("click", (e) => {
      if (!liveResults.contains(e.target) && e.target !== liveInput) {
        liveResults.classList.add("d-none");
      }
    });
  }

  // ---- Photo preview on upload ----
  const photoInput = document.getElementById("photoInput");
  const photoPreview = document.getElementById("photoPreview");
  if (photoInput && photoPreview) {
    photoInput.addEventListener("change", () => {
      const file = photoInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => { photoPreview.src = e.target.result; };
        reader.readAsDataURL(file);
      }
    });
  }
});
