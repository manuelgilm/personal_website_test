// Contact form submission via the Azure Function /api/contact
(function () {
  'use strict';

  var form = document.getElementById('contact-form');
  if (!form) return;

  var loading = form.querySelector('.loading');
  var errorBox = form.querySelector('.error-message');
  var sentBox = form.querySelector('.sent-message');
  var submitBtn = document.getElementById('contact-submit');

  function show(el) { if (el) el.style.display = 'block'; }
  function hide(el) { if (el) el.style.display = 'none'; }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    hide(errorBox);
    hide(sentBox);

    var name = form.name.value.trim();
    var email = form.email.value.trim();
    var subject = form.subject.value.trim();
    var message = form.message.value.trim();

    if (!name || !email || !subject || !message) {
      errorBox.textContent = 'Please fill in all fields.';
      show(errorBox);
      return;
    }

    var payload = {
      name: name,
      email: email,
      subject: subject,
      message: message,
      // honeypot field intentionally left empty
      website: form.website ? form.website.value : ''
    };

    submitBtn.disabled = true;
    show(loading);

    fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        if (result.ok && result.data.success) {
          form.reset();
          show(sentBox);
        } else {
          errorBox.textContent = result.data.message || 'Failed to send your message. Please try again.';
          show(errorBox);
        }
      })
      .catch(function () {
        errorBox.textContent = 'Failed to connect to the server. Please try again later.';
        show(errorBox);
      })
      .finally(function () {
        hide(loading);
        submitBtn.disabled = false;
      });
  });
})();