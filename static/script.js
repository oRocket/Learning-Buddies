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

function togglePassword(inputId) {
    var x = document.getElementById(inputId);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}


document.getElementById('saveButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Extract form data from each form and combine into a single object
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
    }).then(response => {
        if (response.ok) {
            // Handle success (e.g., display a success message)
            alert('Profile saved successfully!');
        } else {
            // Handle error (e.g., display an error message)
            alert('Failed to save profile. Please try again.');
        }
    }).catch(error => {
        console.error('Error:', error);
        // Handle error (e.g., display an error message)
        alert('An unexpected error occurred. Please try again later.');
    });
});

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
