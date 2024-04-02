const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navbar');

if (bar) {
    bar.addEventListener("click", () => {
        nav.classList.add("active");
    })
}

if (close) {
    close.addEventListener("click", () => {
        nav.classList.remove("active");
    })
}

// Add an event listener to the logout link to trigger form submission
document.addEventListener("DOMContentLoaded", function() {
    var logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', function() {
            document.getElementById('logoutForm').submit();
        });
    }
});


function togglePassword(inputId) {
    var x = document.getElementById(inputId);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

// Profile picture
function previewProfilePicture(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Show the profile picture container
            document.getElementById('profile-picture-container').style.display = 'block';
            
            // Set the source of the image
            document.getElementById('profile-picture-preview').src = e.target.result;

            // Store the image data in localStorage
            localStorage.setItem('profilePicture', e.target.result);
        };
        reader.readAsDataURL(file);
    }
}

// Retrieve profile picture from localStorage on page load
window.onload = function() {
    const profilePicture = localStorage.getItem('profilePicture');
    if (profilePicture) {
        document.getElementById('profile-picture-container').style.display = 'block'; // Show the profile picture container
        document.getElementById('profile-picture-preview').src = profilePicture; // Set the source of the image
    }
};


document.getElementById('level_of_education').addEventListener('change', function() {
    var selectedValue = this.value;
    var allCourseSections = document.querySelectorAll('.course-section');
    allCourseSections.forEach(function(section) {
        section.style.display = 'none';
    });
    document.getElementById(selectedValue.toLowerCase().replace(' ', '_') + '_courses').style.display = 'block';
});


document.getElementById('saveButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Extract form data from all forms and combine into a single object
    const formData = {
        ...extractFormData('profileForm1'),
        ...extractFormData('profileForm2'),
        ...extractFormData('profileForm3')
    };

    // Send the form data to the server for saving
    fetch('/profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            // Handle success (e.g., display a success message)
            alert('Profile saved successfully!');
        } else {
            // Handle error (e.g., display an error message)
            alert('Failed to save profile. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error (e.g., display an error message)
        alert('An unexpected error occurred. Please try again later.');
    });
});

// Function to extract form data
function extractFormData(formId) {
    const formData = {};
    const form = document.getElementById(formId);
    if (!form) return formData;
    
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.name) {
            formData[input.name] = input.value;
        }
    });
    return formData;
}


// Function to extract form data
function extractFormData(formId) {
    const formData = {};
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input, select, textarea');

    inputs.forEach(input => {
        formData[input.name] = input.value;
    });

    return formData;
}
