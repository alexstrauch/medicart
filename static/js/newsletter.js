document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletter-form');
    const submitButton = document.getElementById('newsletter-submit');
    const buttonText = submitButton.querySelector('.button-text');
    const spinner = submitButton.querySelector('.spinner-border');
    const feedbackDiv = document.querySelector('.newsletter-feedback');

    function setLoading(isLoading) {
        if (isLoading) {
            buttonText.textContent = 'Subscribing...';
            spinner.classList.remove('d-none');
            submitButton.disabled = true;
        } else {
            buttonText.textContent = 'Subscribe';
            spinner.classList.add('d-none');
            submitButton.disabled = false;
        }
    }

    function showFeedback(message, isSuccess) {
        feedbackDiv.textContent = message;
        feedbackDiv.className = `newsletter-feedback mt-2 alert ${isSuccess ? 'alert-success' : 'alert-danger'}`;
        
        // Clear feedback after 5 seconds
        setTimeout(() => {
            feedbackDiv.textContent = '';
            feedbackDiv.className = 'newsletter-feedback mt-2';
        }, 5000);
    }

    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        setLoading(true);

        const formData = new FormData(this);
        const csrfToken = formData.get('csrfmiddlewaretoken');

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            setLoading(false);
            if (data.success) {
                showFeedback(data.message, true);
                newsletterForm.reset();
            } else {
                showFeedback(data.message || 'An error occurred. Please try again.', false);
            }
        })
        .catch(error => {
            setLoading(false);
            showFeedback('An error occurred. Please try again.', false);
            console.error('Newsletter subscription error:', error);
        });
    });
});
