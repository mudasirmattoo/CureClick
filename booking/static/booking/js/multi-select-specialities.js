// document.addEventListener('DOMContentLoaded', function() {
//     const specialtySelect = document.querySelector('.multi-select-specialities');
    
//     // Create a custom dropdown container
//     const dropdownContainer = document.createElement('div');
//     dropdownContainer.className = 'relative w-full';
//     specialtySelect.parentNode.insertBefore(dropdownContainer, specialtySelect);
    
//     // Create selected items display
//     const selectedDisplay = document.createElement('div');
//     selectedDisplay.className = 'border rounded w-full py-2 px-3 text-gray-700 cursor-pointer shadow appearance-none leading-tight focus:outline-none focus:shadow-outline text-center';
//     dropdownContainer.appendChild(selectedDisplay);
    
//     // Create dropdown options container
//     const optionsContainer = document.createElement('div');
//     optionsContainer.className = 'hidden absolute z-10 w-full bg-white border rounded shadow-lg max-h-60 overflow-y-auto';
//     dropdownContainer.appendChild(optionsContainer);
    
//     // Hide original select
//     specialtySelect.style.display = 'none';
    
//     // Populate options
//     Array.from(specialtySelect.options).forEach(option => {
//         const optionElement = document.createElement('div');
//         optionElement.className = 'flex items-center p-2 hover:bg-gray-100 cursor-pointer';
        
//         const checkbox = document.createElement('input');
//         checkbox.type = 'checkbox';
//         checkbox.value = option.value;
//         checkbox.checked = option.selected;
//         checkbox.className = 'mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500';
        
//         const label = document.createElement('label');
//         label.className = 'flex items-center text-sm text-gray-700 cursor-pointer';
//         label.appendChild(checkbox);
        
//         const labelText = document.createElement('span');
//         labelText.textContent = option.text;
//         labelText.className = 'ml-2';
//         label.appendChild(labelText);
        
//         optionElement.appendChild(label);
//         optionsContainer.appendChild(optionElement);
        
//         // Toggle selection when label is clicked
//         label.addEventListener('click', function(e) {
//             e.stopPropagation();
//             checkbox.checked = !checkbox.checked;
//             updateSelectedDisplay();
//             updateOriginalSelect();
//         });
//     });
    
//     // Update selected display
//     function updateSelectedDisplay() {
//         const selectedOptions = Array.from(optionsContainer.querySelectorAll('input:checked'))
//             .map(input => input.nextElementSibling.textContent);
        
//         selectedDisplay.textContent = selectedOptions.length > 0 
//             ? selectedOptions.join(', ') 
//             : 'Select Specialities';
        
//         // Add visual indication of selection
//         selectedDisplay.classList.toggle('text-gray-400', selectedOptions.length === 0);
//         selectedDisplay.classList.toggle('text-gray-700', selectedOptions.length > 0);
//     }
    
//     // Update original select element
//     function updateOriginalSelect() {
//         Array.from(specialtySelect.options).forEach(option => {
//             const correspondingCheckbox = optionsContainer.querySelector(`input[value="${option.value}"]`);
//             option.selected = correspondingCheckbox.checked;
//         });
//     }
    
//     // Toggle dropdown
//     selectedDisplay.addEventListener('click', function() {
//         optionsContainer.classList.toggle('hidden');
//     });
    
//     // Close dropdown when clicking outside
//     document.addEventListener('click', function(e) {
//         if (!dropdownContainer.contains(e.target)) {
//             optionsContainer.classList.add('hidden');
//         }
//     });
    
//     // Initial display update
//     updateSelectedDisplay();
// });