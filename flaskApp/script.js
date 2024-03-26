
function updateDropdown(type, value) {
    if (type === 'Cell Lines') {
        document.getElementById('selectedCellLine').textContent = value;
    } else if (type === 'Drugs') {
        document.getElementById('selectedDrug').textContent = value;
    }
}



