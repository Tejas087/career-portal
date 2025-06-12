document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.querySelector('.logout-trigger');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior
            document.getElementById('logoutForm').submit(); // Submit the hidden form
        });
    }
});