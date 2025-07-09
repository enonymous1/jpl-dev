document.addEventListener('DOMContentLoaded', function() {
    // Local storage key for the checklist data
    const STORAGE_KEY = 'gsa_mas_checklist_data';
    
    // Load saved data from local storage
    function loadChecklistData() {
        const savedData = localStorage.getItem(STORAGE_KEY);
        return savedData ? JSON.parse(savedData) : {};
    }
    
    // Save data to local storage
    function saveChecklistData(data) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        showSaveIndicator();
    }
    
    // Show save indicator
    function showSaveIndicator() {
        const indicator = document.getElementById('save-indicator');
        if (indicator) {
            indicator.textContent = 'Saved ✓';
            indicator.className = 'save-indicator saved show';
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 2000);
        }
    }
    
    // Get current checklist state
    function getCurrentState() {
        const state = {
            formData: {},
            checkboxes: {},
            notes: {}
        };
        
        // Save form data
        const formElements = document.querySelectorAll('#offer-form input, #offer-form select');
        formElements.forEach(element => {
            state.formData[element.id] = element.value;
        });
        
        // Save checkbox states
        const checkboxes = document.querySelectorAll('.checklist-card-header input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            state.checkboxes[checkbox.id] = checkbox.checked;
        });
        
        // Save notes from Quill editors
        Object.keys(quillInstances).forEach(editorId => {
            const quill = quillInstances[editorId];
            state.notes[editorId] = quill.getContents();
        });
        
        return state;
    }
    
    // Load saved state
    function loadSavedState() {
        const savedState = loadChecklistData();
        
        // Load form data
        if (savedState.formData) {
            Object.keys(savedState.formData).forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    element.value = savedState.formData[id];
                    // Trigger change event for button groups
                    if (element.type === 'hidden' && element.id === 'commodity_type') {
                        const btnGroup = document.getElementById('commodity_type_group');
                        const buttons = btnGroup.querySelectorAll('.btn');
                        buttons.forEach(btn => {
                            btn.classList.remove('active');
                            if (btn.textContent === savedState.formData[id]) {
                                btn.classList.add('active');
                            }
                        });
                    }
                }
            });
        }
        
        // Load checkbox states
        if (savedState.checkboxes) {
            Object.keys(savedState.checkboxes).forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.checked = savedState.checkboxes[id];
                    updateModalStatus(checkbox);
                }
            });
        }
        
        // Load notes (will be loaded when modals open)
        return savedState;
    }
    
    // Auto-save functionality
    function setupAutoSave() {
        // Save on form input changes
        const formElements = document.querySelectorAll('#offer-form input, #offer-form select');
        formElements.forEach(element => {
            element.addEventListener('input', () => {
                saveChecklistData(getCurrentState());
            });
        });
        
        // Save on checkbox changes
        const checkboxes = document.querySelectorAll('.checklist-card-header input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                saveChecklistData(getCurrentState());
            });
        });
    }
    
    // Export/Import functionality
    function exportData() {
        const data = getCurrentState();
        const dataStr = JSON.stringify(data, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'gsa_mas_checklist_backup.json';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
    
    function importData(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const importedData = JSON.parse(e.target.result);
                    localStorage.setItem(STORAGE_KEY, JSON.stringify(importedData));
                    location.reload(); // Reload to apply imported data
                } catch (error) {
                    alert('Error importing data: Invalid file format');
                }
            };
            reader.readAsText(file);
        }
    }
    
    function clearData() {
        if (confirm('Are you sure you want to clear all saved data? This action cannot be undone.')) {
            localStorage.removeItem(STORAGE_KEY);
            location.reload();
        }
    }

    // Commodity type button group logic
    var btnGroup = document.getElementById('commodity_type_group');
    var hiddenInput = document.getElementById('commodity_type');

    btnGroup.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn')) {
            // Remove active class from all buttons
            var buttons = btnGroup.querySelectorAll('.btn');
            buttons.forEach(function(button) {
                button.classList.remove('active');
            });

            // Add active class to the clicked button
            e.target.classList.add('active');

            // Update the hidden input value
            hiddenInput.value = e.target.textContent;
            
            // Auto-save
            saveChecklistData(getCurrentState());
        }
    });

    // Modal logic
    const checklistItems = document.querySelectorAll('.checklist-item');
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close-button');
    const checkboxes = document.querySelectorAll('.checklist-card-header input[type="checkbox"]');

    // Progress tracking
    function updateProgress() {
        const checkboxes = document.querySelectorAll('.checklist-card-header input[type="checkbox"]');
        const totalCount = checkboxes.length;
        const completedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
        const percentage = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;
        
        // Update overall progress
        const progressCount = document.getElementById('progress-count');
        const totalCountElement = document.getElementById('total-count');
        const progressFill = document.getElementById('progress-fill');
        
        if (progressCount) progressCount.textContent = completedCount;
        if (totalCountElement) totalCountElement.textContent = totalCount;
        if (progressFill) progressFill.style.width = `${percentage}%`;
        
        // Update section progress
        updateSectionProgress();
    }
    
    function updateSectionProgress() {
        const sections = document.querySelectorAll('.checklist-section-header');
        const sectionProgressList = document.getElementById('section-progress-list');
        
        if (!sectionProgressList) return;
        
        // Clear existing progress items
        sectionProgressList.innerHTML = '';
        
        sections.forEach((sectionHeader, index) => {
            const sectionName = sectionHeader.getAttribute('data-section');
            const badge = document.getElementById(`badge-${index}`);
            
            // Find all checkboxes in this section
            let nextElement = sectionHeader.nextElementSibling;
            const sectionCheckboxes = [];
            
            while (nextElement && !nextElement.classList.contains('checklist-section-header')) {
                const checkbox = nextElement.querySelector('.checklist-card-header input[type="checkbox"]');
                if (checkbox) {
                    sectionCheckboxes.push(checkbox);
                }
                nextElement = nextElement.nextElementSibling;
            }
            
            const totalInSection = sectionCheckboxes.length;
            const completedInSection = sectionCheckboxes.filter(cb => cb.checked).length;
            const sectionPercentage = totalInSection > 0 ? (completedInSection / totalInSection) * 100 : 0;
            
            // Update section badge
            if (badge) {
                badge.textContent = `${completedInSection}/${totalInSection}`;
                badge.className = 'section-badge';
                if (completedInSection === totalInSection && totalInSection > 0) {
                    badge.classList.add('completed');
                } else if (completedInSection > 0) {
                    badge.classList.add('partial');
                }
            }
            
            // Create section progress item
            const progressItem = document.createElement('div');
            progressItem.className = 'section-progress-item';
            progressItem.innerHTML = `
                <span class="section-name">${sectionName}</span>
                <div style="display: flex; align-items: center;">
                    <span class="section-count">${completedInSection}/${totalInSection}</span>
                    <div class="section-mini-bar">
                        <div class="section-mini-fill" style="width: ${sectionPercentage}%"></div>
                    </div>
                </div>
            `;
            
            sectionProgressList.appendChild(progressItem);
        });
    }

    function updateModalStatus(checkbox) {
        const line_number = checkbox.id.split('-')[1];
        const status_span = document.getElementById(`status-${line_number}`);
        if (status_span) {
            if (checkbox.checked) {
                status_span.textContent = 'Complete';
                status_span.className = 'modal-status complete';
            } else {
                status_span.textContent = 'Incomplete';
                status_span.className = 'modal-status incomplete';
            }
        }
        // Update progress whenever checkbox state changes
        updateProgress();
    }

    checklistItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const modal = document.querySelector(item.dataset.modalTarget);
            const line_number = item.getAttribute('for').split('-')[1];
            const checkbox = document.getElementById(`item-${line_number}`);
            updateModalStatus(checkbox);
            modal.style.display = "block";
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal');
            modal.style.display = "none";
        });
    });

    window.addEventListener('click', (event) => {
        modals.forEach(modal => {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        });
    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateModalStatus(checkbox);
        });
    });

    // Initialize Quill editor on modal open
    const quillInstances = {};
    const savedState = loadSavedState();
    
    checklistItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const modal = document.querySelector(item.dataset.modalTarget);
            const editorDiv = modal.querySelector('.note-editor');
            
            // Check if the editor is already initialized
            if (!quillInstances[editorDiv.id]) {
                quillInstances[editorDiv.id] = new Quill(`#${editorDiv.id}`, {
                    theme: 'snow',
                    placeholder: 'Add your notes here...',
                    modules: {
                        toolbar: [
                            ['bold', 'italic', 'underline', 'strike'],
                            ['blockquote', 'code-block'],
                            [{ 'header': 1 }, { 'header': 2 }],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                            [{ 'script': 'sub'}, { 'script': 'super' }],
                            [{ 'indent': '-1'}, { 'indent': '+1' }],
                            ['link'],
                            ['clean']
                        ]
                    }
                });
                
                // Load saved content if available
                if (savedState.notes && savedState.notes[editorDiv.id]) {
                    quillInstances[editorDiv.id].setContents(savedState.notes[editorDiv.id]);
                }
                
                // Auto-save on content change
                quillInstances[editorDiv.id].on('text-change', function() {
                    saveChecklistData(getCurrentState());
                });
            }
        });
    });
    
    // Setup auto-save
    setupAutoSave();
    
    // Initialize progress display
    updateProgress();
    
    // Add event listeners for export/import buttons
    const exportBtn = document.getElementById('export-btn');
    const importBtn = document.getElementById('import-btn');
    const importFile = document.getElementById('import-file');
    const clearBtn = document.getElementById('clear-btn');
    
    if (exportBtn) exportBtn.addEventListener('click', exportData);
    if (importBtn) importBtn.addEventListener('click', () => importFile.click());
    if (importFile) importFile.addEventListener('change', importData);
    if (clearBtn) clearBtn.addEventListener('click', clearData);
});
