document.addEventListener('DOMContentLoaded', function() {
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const mobileMenu = document.getElementById('mobile-nav');
        const navbarToggler = document.querySelector('.navbar-toggler');
        
        // If menu is open and click is outside menu and not on burger icon
        if (mobileMenu && mobileMenu.classList.contains('show') && 
            !mobileMenu.contains(event.target) && 
            !navbarToggler.contains(event.target)) {
            // Create a new bootstrap collapse instance and hide it
            const bsCollapse = new bootstrap.Collapse(mobileMenu);
            bsCollapse.hide();
        }
    });
});
