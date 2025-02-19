function toggleMedicationFields() {
    var medicationSelect = document.getElementById('medication');
    var medicationFields = document.getElementById('medication-fields');
    if (medicationSelect.value === 'yes') {
        medicationFields.style.display = 'block';
    } else {
        medicationFields.style.display = 'none';
    }
}