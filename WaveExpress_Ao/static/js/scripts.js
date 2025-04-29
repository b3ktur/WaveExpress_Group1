// WaveExpress Ferry System JavaScript

// Auto-hide alerts after a few seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Initialize any tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize any date pickers
    const datePickers = document.querySelectorAll('input[type="date"]');
    if (datePickers.length > 0) {
        // Set default date to today for empty date inputs
        datePickers.forEach(function(picker) {
            if (!picker.value) {
                const today = new Date().toISOString().split('T')[0];
                picker.value = today;
            }
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Handle payment method changes in ticket payment form
    const paymentMethodSelect = document.getElementById('id_payment_method');
    if (paymentMethodSelect) {
        const cardFields = document.querySelectorAll('.card-field');
        
        function toggleCardFields() {
            const selectedMethod = paymentMethodSelect.value;
            if (selectedMethod === 'CREDIT_CARD' || selectedMethod === 'DEBIT_CARD') {
                cardFields.forEach(field => field.classList.remove('d-none'));
            } else {
                cardFields.forEach(field => field.classList.add('d-none'));
            }
        }
        
        // Initial state
        toggleCardFields();
        
        // Listen for changes
        paymentMethodSelect.addEventListener('change', toggleCardFields);
    }
});
