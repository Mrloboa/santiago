document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const submitButton = this.querySelector('button[type="submit"]');
    const originalContent = submitButton.innerHTML;
    
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="tex">Enviando...</span><span class="circle"></span>';
    submitButton.style.opacity = '0.7';

    const formData = new FormData(this);

    fetch('/send_email', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showFlashMessage(data.message, 'success');
            this.reset();
        } else {
            showFlashMessage(data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showFlashMessage('Hubo un error de conexión. Revisa tu internet e intenta nuevamente.', 'danger');
    })
    .finally(() => {
        submitButton.disabled = false;
        submitButton.innerHTML = originalContent;
        submitButton.style.opacity = '1';
    });
});

function showFlashMessage(message, category) {
    const flashContainer = document.getElementById('flash-messages');
    if (!flashContainer) return;

    flashContainer.innerHTML = '';
    const flashMessage = document.createElement('div');
    
    flashMessage.style.padding = '15px';
    flashMessage.style.marginBottom = '20px';
    flashMessage.style.borderRadius = '10px';
    flashMessage.style.color = '#000';
    flashMessage.style.fontWeight = 'bold';
    flashMessage.style.textAlign = 'center';
    
    if (category === 'success') {
        flashMessage.style.backgroundColor = '#39FF14'; 
        flashMessage.style.boxShadow = '0 0 15px rgba(57, 255, 20, 0.4)';
    } else {
        flashMessage.style.backgroundColor = '#FF3939';
        flashMessage.style.boxShadow = '0 0 15px rgba(255, 57, 57, 0.4)';
    }
    
    flashMessage.textContent = message;
    flashContainer.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.style.opacity = '0';
        flashMessage.style.transition = 'opacity 0.5s ease';
        setTimeout(() => flashMessage.remove(), 500);
    }, 5000);
}