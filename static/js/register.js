// Form validation and phone number formatting
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    
    // Phone validation
    const phoneInput = document.querySelector('input[name="phone"]');
    phoneInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
        // Remove error styling when user starts typing
        this.classList.remove('is-invalid');
    });

    const altPhoneInput = document.querySelector('input[name="alt_phone"]');
    if (altPhoneInput) {
        altPhoneInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }

    // Remove error styling when user interacts with fields
    const allInputs = form.querySelectorAll('input, textarea, select');
    allInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
        input.addEventListener('change', function() {
            this.classList.remove('is-invalid');
        });
    });

    // Form submission validation
    form.addEventListener('submit', function(e) {
        let isValid = true;
        let errorMessage = '';
        let firstInvalidField = null;

        // Remove all previous error styling
        allInputs.forEach(input => input.classList.remove('is-invalid'));

        // Get all required fields
        const nameInput = document.querySelector('input[name="name"]');
        const addressInput = document.querySelector('textarea[name="address"]');
        const phoneInput = document.querySelector('input[name="phone"]');
        const dobInput = document.querySelector('input[name="dob"]');
        const bloodGroupInput = document.querySelector('select[name="blood_group"]');
        const diseaseInputs = document.querySelectorAll('input[name="disease"]');
        const passwordInput = document.querySelector('input[name="password"]');

        const name = nameInput.value.trim();
        const address = addressInput.value.trim();
        const phone = phoneInput.value.trim();
        const dob = dobInput.value;
        const bloodGroup = bloodGroupInput.value;
        const disease = document.querySelector('input[name="disease"]:checked');
        const password = passwordInput.value;

        // Validate each field
        if (!name) {
            errorMessage = 'Please enter your name';
            nameInput.classList.add('is-invalid');
            firstInvalidField = nameInput;
            isValid = false;
        } else if (!address) {
            errorMessage = 'Please enter your address';
            addressInput.classList.add('is-invalid');
            firstInvalidField = addressInput;
            isValid = false;
        } else if (!phone) {
            errorMessage = 'Please enter your phone number';
            phoneInput.classList.add('is-invalid');
            firstInvalidField = phoneInput;
            isValid = false;
        } else if (phone.length !== 10) {
            errorMessage = 'Phone number must be exactly 10 digits';
            phoneInput.classList.add('is-invalid');
            firstInvalidField = phoneInput;
            isValid = false;
        } else if (!dob) {
            errorMessage = 'Please select your date of birth';
            dobInput.classList.add('is-invalid');
            firstInvalidField = dobInput;
            isValid = false;
        } else if (!bloodGroup) {
            errorMessage = 'Please select your blood group';
            bloodGroupInput.classList.add('is-invalid');
            firstInvalidField = bloodGroupInput;
            isValid = false;
        } else if (!disease) {
            errorMessage = 'Please select if you have any disease (Yes or No)';
            diseaseInputs.forEach(input => input.classList.add('is-invalid'));
            firstInvalidField = diseaseInputs[0];
            isValid = false;
        } else if (!password) {
            errorMessage = 'Please enter a password';
            passwordInput.classList.add('is-invalid');
            firstInvalidField = passwordInput;
            isValid = false;
        } else if (password.length < 6) {
            errorMessage = 'Password must be at least 6 characters long';
            passwordInput.classList.add('is-invalid');
            firstInvalidField = passwordInput;
            isValid = false;
        }

        // Show error if validation fails
        if (!isValid) {
            e.preventDefault();
            
            // Remove existing error alert if any
            const existingAlert = document.querySelector('.alert-danger.validation-error');
            if (existingAlert) {
                existingAlert.remove();
            }

            // Create and show error alert
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show validation-error';
            alertDiv.innerHTML = `
                <strong>Error:</strong> ${errorMessage}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            form.insertBefore(alertDiv, form.firstChild);
            
            // Scroll to the first invalid field
            if (firstInvalidField) {
                firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                setTimeout(() => firstInvalidField.focus(), 500);
            }
        }
    });
});
