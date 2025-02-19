function toggleMedicationFields() {
    var medicationCheckbox = document.getElementById('medication');
    var medicationFields = document.getElementById('medication-fields');
    if (medicationCheckbox.checked) {
        medicationFields.style.display = 'block';
    } else {
        medicationFields.style.display = 'none';
    }
}