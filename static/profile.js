// Add your JavaScript code here
document.getElementById('profileForm').addEventListener('submit', function(event) {
    // Prevent the form from submitting
    event.preventDefault();

    // You can add form validation or submission handling here
    // For example, you could use JavaScript to validate the form inputs before submission
    // or send the form data to a server using AJAX
    // For demonstration purposes, we're just preventing the form from submitting in this example
    console.log('Form submitted (but not really because this is a demo)');
});
