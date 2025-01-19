document.addEventListener('DOMContentLoaded', function() {
    // Get all section buttons and content sections
    const sectionButtons = document.querySelectorAll('.list-group-item');
    const sections = document.querySelectorAll('.section-content');

    // Function to show selected section and hide others
    function showSection(sectionId) {
        // Hide all sections
        sections.forEach(section => {
            section.classList.add('d-none');
        });

        // Show selected section
        const selectedSection = document.getElementById(sectionId);
        if (selectedSection) {
            selectedSection.classList.remove('d-none');
        }

        // Update active state of buttons
        sectionButtons.forEach(button => {
            if (button.dataset.section === sectionId) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
    }

    // Add click event listeners to all section buttons
    sectionButtons.forEach(button => {
        button.addEventListener('click', function() {
            showSection(this.dataset.section);
        });
    });

    // Handle cancel button in delete account section
    const cancelDeleteButton = document.querySelector('#delete-account button[data-section="profile-info"]');
    if (cancelDeleteButton) {
        cancelDeleteButton.addEventListener('click', function() {
            showSection('profile-info');
        });
    }
});
