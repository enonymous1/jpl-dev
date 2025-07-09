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
        
        // Save notes from Editor.js instances (called when manually saving)
        // Notes are saved individually when the save button is clicked
        
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
    const clickableContent = document.querySelectorAll('.clickable-content');

    // Content modal functionality
    clickableContent.forEach(content => {
        content.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation(); // Prevent triggering parent click events
            const modalTarget = content.getAttribute('data-content-modal');
            const modal = document.querySelector(modalTarget);
            if (modal) {
                modal.style.display = "block";
            }
        });
    });

    // Progress tracking
    function updateProgress() {
        const checkboxes = document.querySelectorAll('.checklist-card-header input[type="checkbox"]');
        const totalCount = checkboxes.length;
        const completedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
        const percentage = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;
        
        // Update compact progress indicator
        const progressCount = document.getElementById('progress-count');
        const totalCountElement = document.getElementById('total-count');
        const progressFill = document.getElementById('progress-fill');
        const progressIndicator = document.getElementById('progress-indicator-compact');
        
        if (progressCount) progressCount.textContent = completedCount;
        if (totalCountElement) totalCountElement.textContent = totalCount;
        if (progressFill) progressFill.style.width = `${percentage}%`;
        
        // Show progress indicator with animation after first update
        if (progressIndicator && !progressIndicator.classList.contains('show')) {
            setTimeout(() => {
                progressIndicator.classList.add('show');
            }, 500); // Small delay for better UX
        }
        
        // Update section badges
        updateSectionBadges();
    }
    
    function updateSectionBadges() {
        const sections = document.querySelectorAll('.section-container');
        
        sections.forEach((sectionContainer, index) => {
            const badge = document.getElementById(`badge-${index}`);
            
            // Find all checkboxes in this section
            const sectionCheckboxes = sectionContainer.querySelectorAll('.checklist-card-header input[type="checkbox"]');
            const totalInSection = sectionCheckboxes.length;
            const completedInSection = Array.from(sectionCheckboxes).filter(cb => cb.checked).length;
            
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
        });
    }
    
    // Accordion functionality
    function setupAccordions() {
        const sectionHeaders = document.querySelectorAll('.accordion-header');
        
        sectionHeaders.forEach((header, index) => {
            const toggle = header.querySelector('.accordion-toggle');
            const sectionContent = document.getElementById(`section-${index}`);
            
            // Set initial state for first section
            if (index === 0) {
                toggle.classList.add('rotated');
            }
            
            header.addEventListener('click', () => {
                const isExpanded = sectionContent.classList.contains('expanded');
                
                if (isExpanded) {
                    // Collapse
                    sectionContent.classList.remove('expanded');
                    toggle.classList.remove('rotated');
                } else {
                    // Expand
                    sectionContent.classList.add('expanded');
                    toggle.classList.add('rotated');
                }
            });
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

    // Initialize Editor.js on modal open
    const editorInstances = {};
    const savedState = loadSavedState();
    
    checklistItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const modal = document.querySelector(item.dataset.modalTarget);
            const editorDiv = modal.querySelector('.note-editor');
            
            // Check if the editor is already initialized
            if (!editorInstances[editorDiv.id]) {
                // Check if Quill is available
                if (typeof Quill === 'undefined') {
                    console.log('Quill not loaded, falling back to simple textarea');
                    // Fallback to simple textarea if Quill fails to load
                    const textarea = document.createElement('textarea');
                    textarea.placeholder = 'Add your notes here...';
                    textarea.style.width = '100%';
                    textarea.style.minHeight = '150px';
                    textarea.style.padding = '12px';
                    textarea.style.border = '1px solid #ccc';
                    textarea.style.borderRadius = '4px';
                    textarea.style.fontFamily = 'inherit';
                    textarea.style.resize = 'vertical';
                    
                    // Load saved content if available
                    if (savedState.notes && savedState.notes[editorDiv.id]) {
                        textarea.value = savedState.notes[editorDiv.id];
                    }
                    
                    editorDiv.innerHTML = '';
                    editorDiv.appendChild(textarea);
                    editorInstances[editorDiv.id] = {
                        element: textarea,
                        getContents: () => textarea.value,
                        setContents: (content) => { textarea.value = content || ''; }
                    };
                    return;
                }
                
                try {
                    // Clear existing content and prepare the editor div
                    editorDiv.innerHTML = '';
                    editorDiv.style.minHeight = '150px';
                    editorDiv.style.maxHeight = '300px';
                    editorDiv.style.border = '1px solid #ccc';
                    editorDiv.style.borderRadius = '4px';
                    editorDiv.style.backgroundColor = 'white';
                    
                    // Initialize Quill directly on the editor div
                    const quill = new Quill(editorDiv, {
                        theme: 'snow',
                        placeholder: 'Add your notes here...',
                        modules: {
                            toolbar: [
                                ['bold', 'italic', 'underline', 'strike'],
                                ['blockquote', 'code-block'],
                                [{ 'color': [] }, { 'background': [] }],
                                ['clean']
                            ]
                        },
                        formats: ['bold', 'italic', 'underline', 'strike', 'blockquote', 'code-block', 'color', 'background']
                    });
                    
                    // Load saved content if available
                    if (savedState.notes && savedState.notes[editorDiv.id]) {
                        try {
                            // Try to parse as Delta (Quill's native format)
                            const savedData = savedState.notes[editorDiv.id];
                            if (typeof savedData === 'object' && savedData.ops) {
                                quill.setContents(savedData);
                            } else if (typeof savedData === 'string') {
                                quill.setText(savedData);
                            }
                        } catch (error) {
                            console.error('Error loading saved content:', error);
                            // Fallback to plain text
                            if (typeof savedState.notes[editorDiv.id] === 'string') {
                                quill.setText(savedState.notes[editorDiv.id]);
                            }
                        }
                    }
                    
                    // Store Quill instance
                    editorInstances[editorDiv.id] = {
                        quill: quill,
                        getContents: () => quill.getContents(),
                        setContents: (content) => {
                            if (typeof content === 'object' && content.ops) {
                                quill.setContents(content);
                            } else {
                                quill.setText(content || '');
                            }
                        }
                    };
                    
                } catch (error) {
                    console.error('Failed to initialize Quill:', error);
                    // Fallback to simple textarea on error
                    const textarea = document.createElement('textarea');
                    textarea.placeholder = 'Add your notes here...';
                    textarea.style.width = '100%';
                    textarea.style.minHeight = '150px';
                    textarea.style.padding = '12px';
                    textarea.style.border = '1px solid #ccc';
                    textarea.style.borderRadius = '4px';
                    textarea.style.fontFamily = 'inherit';
                    textarea.style.resize = 'vertical';
                    
                    // Load saved content if available
                    if (savedState.notes && savedState.notes[editorDiv.id]) {
                        const savedData = savedState.notes[editorDiv.id];
                        if (typeof savedData === 'object' && savedData.ops) {
                            // Convert Delta to plain text
                            textarea.value = savedData.ops.map(op => op.insert || '').join('');
                        } else {
                            textarea.value = savedData || '';
                        }
                    }
                    
                    editorDiv.innerHTML = '';
                    editorDiv.appendChild(textarea);
                    editorInstances[editorDiv.id] = {
                        element: textarea,
                        getContents: () => textarea.value,
                        setContents: (content) => { 
                            if (typeof content === 'object' && content.ops) {
                                textarea.value = content.ops.map(op => op.insert || '').join('');
                            } else {
                                textarea.value = content || '';
                            }
                        }
                    };
                }
            }
        });
    });
    
    // Setup auto-save
    setupAutoSave();
    
    // Setup accordion functionality
    setupAccordions();
    
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
    
    // Setup manual save functionality for notes
    function setupManualNoteSave() {
        const saveButtons = document.querySelectorAll('.save-notes-btn');
        saveButtons.forEach(button => {
            button.addEventListener('click', async function() {
                const itemId = this.dataset.itemId;
                const editorId = `note-${itemId}`;
                const editor = editorInstances[editorId];
                
                if (editor) {
                    try {
                        // Get the current state
                        const state = getCurrentState();
                        
                        // Save the editor content
                        if (editor.getContents) {
                            state.notes[editorId] = editor.getContents();
                        } else if (editor.element) {
                            // Fallback textarea
                            state.notes[editorId] = editor.element.value || '';
                        }
                        
                        // Save to localStorage
                        saveChecklistData(state);
                        
                        // Show feedback
                        this.textContent = 'Saved!';
                        this.classList.add('saved');
                        
                        setTimeout(() => {
                            this.textContent = 'Save Notes';
                            this.classList.remove('saved');
                        }, 2000);
                        
                    } catch (error) {
                        console.error('Error saving notes:', error);
                        this.textContent = 'Error saving';
                        this.style.background = '#dc3545';
                        
                        setTimeout(() => {
                            this.textContent = 'Save Notes';
                            this.style.background = '';
                        }, 2000);
                    }
                }
            });
        });
    }
    
    // Initialize manual save after a short delay to ensure buttons are rendered
    setTimeout(setupManualNoteSave, 100);
});
