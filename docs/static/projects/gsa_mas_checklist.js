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
        const headerSaveBtn = document.getElementById('save-btn');
        
        // Legacy save indicator (if present)
        if (indicator) {
            indicator.textContent = 'Saved ✓';
            indicator.className = 'save-indicator saved show';
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 2000);
        }
        
        // Header save button feedback
        if (headerSaveBtn) {
            headerSaveBtn.classList.add('saved');
            setTimeout(() => {
                headerSaveBtn.classList.remove('saved');
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
        console.log('Setting up accordions...');
        const sectionHeaders = document.querySelectorAll('.accordion-header');
        console.log('Found section headers:', sectionHeaders.length);
        
        sectionHeaders.forEach((header, index) => {
            const toggle = header.querySelector('.accordion-toggle');
            const sectionContent = document.getElementById(`section-${index}`);
            
            console.log(`Setting up section ${index}:`, header, sectionContent);
            
            // Set initial state for first section
            if (index === 0) {
                toggle.classList.add('rotated');
            }
            
            header.addEventListener('click', () => {
                console.log(`Accordion clicked for section ${index}`);
                const isExpanded = sectionContent.classList.contains('expanded');
                
                if (isExpanded) {
                    // Collapse
                    console.log('Collapsing section');
                    sectionContent.classList.remove('expanded');
                    toggle.classList.remove('rotated');
                } else {
                    // Expand
                    console.log('Expanding section');
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
    
    // SINs Selection Modal Functionality
    let sinsData = [];
    let selectedSins = new Set();
    
    // Load SINs data
    async function loadSinsData() {
        try {
            const response = await fetch('/static/projects/gsa_mas_checklist/data/sins_data.json');
            if (!response.ok) {
                throw new Error('Failed to load SINs data');
            }
            sinsData = await response.json();
            populateCategoryFilter();
            renderSinsList();
        } catch (error) {
            console.error('Error loading SINs data:', error);
            document.getElementById('sins-list').innerHTML = 
                '<div class="no-results">Failed to load SINs data. Please try again later.</div>';
        }
    }
    
    // Populate category filter dropdown
    function populateCategoryFilter() {
        const categoryFilter = document.getElementById('sins-category-filter');
        const categories = [...new Set(sinsData.map(sin => sin['Large Category'] || 'Other'))].sort();
        
        categoryFilter.innerHTML = '<option value="">All Categories</option>';
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilter.appendChild(option);
        });
    }
    
    // Filter SINs based on search and all filter criteria
    function filterSins() {
        const searchTerm = document.getElementById('sins-search').value.toLowerCase();
        const selectedCategory = document.getElementById('sins-category-filter').value;
        const selectedCommodity = document.getElementById('sins-commodity-filter').value;
        const selectedStateLocal = document.getElementById('sins-state-local-filter').value;
        const selectedSetAside = document.getElementById('sins-set-aside-filter').value;
        const selectedTdr = document.getElementById('sins-tdr-filter').value;
        const selectedOlm = document.getElementById('sins-olm-filter').value;
        
        return sinsData.filter(sin => {
            const sinNumber = sin._primary_sin || sin.SIN || '';
            const sinTitle = sin['SIN Title'] || '';
            const sinDescription = sin['SIN Descripion'] || '';
            const subcategory = sin.Subcategory || '';
            const keywords = sin._generated_keywords || [];
            const naics = String(sin['List of NAICS'] || '');
            
            // Search filter
            const matchesSearch = !searchTerm || 
                sinNumber.toLowerCase().includes(searchTerm) ||
                sinTitle.toLowerCase().includes(searchTerm) ||
                sinDescription.toLowerCase().includes(searchTerm) ||
                subcategory.toLowerCase().includes(searchTerm) ||
                naics.toLowerCase().includes(searchTerm) ||
                keywords.some(keyword => keyword.toLowerCase().includes(searchTerm));
            
            // Category filter
            const sinCategory = sin['Large Category'] || 'Other';
            const matchesCategory = !selectedCategory || sinCategory === selectedCategory;
            
            // Commodity filter
            const commodityCode = sin['Commodity Code'] || '';
            const matchesCommodity = !selectedCommodity || commodityCode === selectedCommodity;
            
            // State/Local filter
            const stateLocal = sin['State Local'] || '';
            const matchesStateLocal = !selectedStateLocal || stateLocal === selectedStateLocal;
            
            // Set Aside filter
            const setAside = sin['Set Aside'] || '';
            const matchesSetAside = !selectedSetAside || setAside === selectedSetAside;
            
            // TDR filter
            const tdr = sin.TDR || '';
            const matchesTdr = !selectedTdr || tdr === selectedTdr;
            
            // OLM filter
            const olm = sin.OLM || '';
            const matchesOlm = !selectedOlm || olm === selectedOlm;
            
            return matchesSearch && matchesCategory && matchesCommodity && 
                   matchesStateLocal && matchesSetAside && matchesTdr && matchesOlm;
        });
    }
    
    // Render the SINs list
    function renderSinsList() {
        const sinsList = document.getElementById('sins-list');
        const filteredSins = filterSins();
        
        if (filteredSins.length === 0) {
            sinsList.innerHTML = '<div class="no-results">No SINs found matching your criteria.</div>';
            return;
        }
        
        sinsList.innerHTML = '';
        filteredSins.forEach(sin => {
            const sinItem = document.createElement('div');
            sinItem.className = 'sin-item';
            sinItem.dataset.sinNumber = sin._primary_sin;
            
            if (selectedSins.has(sin._primary_sin)) {
                sinItem.classList.add('selected');
            }
            
            // Extract data from the Excel columns
            const sinNumber = sin.SIN || sin._primary_sin || 'N/A';
            const sinTitle = sin['SIN Title'] || 'No title available';
            const sinDescription = sin['SIN Descripion'] || sin['SIN Description'] || 'No description available';
            const largeCategory = sin['Large Category'] || '';
            const largeCategoryCode = sin['Large Category Code '] || sin['Large Category Code'] || '';
            const subcategory = sin.Subcategory || '';
            const subcategoryCode = sin['Subcategory Code'] || '';
            const naicsList = sin['List of NAICS'] || 'Not specified';
            const maxOrderLimit = sin['Maximum Order Limit'];
            const pscCode = sin['PSC Cd'] || 'Not specified';
            const stateLocal = sin['State Local'] === 'Y' ? 'Yes' : sin['State Local'] === 'N' ? 'No' : 'Not specified';
            const setAside = sin['Set Aside'] === 'Y' ? 'Yes' : sin['Set Aside'] === 'N' ? 'No' : 'Not specified';
            const commodityCode = sin['Commodity Code'] || 'Not specified';
            const tdr = sin.TDR === 'Y' ? 'Yes' : sin.TDR === 'N' ? 'No' : 'Not specified';
            const olm = sin.OLM === 'Y' ? 'Yes' : sin.OLM === 'N' ? 'No' : 'Not specified';
            
            // Format the order limit
            let formattedOrderLimit = 'Not specified';
            if (maxOrderLimit && maxOrderLimit !== '' && !isNaN(maxOrderLimit)) {
                const limitNum = parseFloat(maxOrderLimit);
                formattedOrderLimit = '$' + limitNum.toLocaleString();
            }
            
            // Create category display with codes
            const categoryDisplay = `${largeCategory} (${largeCategoryCode.trim()})` + 
                                  (subcategory ? ` > ${subcategory} (${subcategoryCode})` : '');
            
            sinItem.innerHTML = `
                <div class="sin-item-header">
                    <input type="checkbox" class="sin-checkbox" ${selectedSins.has(sin._primary_sin) ? 'checked' : ''}>
                    <div class="sin-main-info">
                        <div class="sin-number">${sinNumber}</div>
                        <div class="sin-category-display"><strong>${categoryDisplay}</strong></div>
                    </div>
                </div>
                <div class="sin-metadata">
                    <div class="sin-metadata-item sin-metadata-full-width">
                        <div class="sin-metadata-label">SIN Title:</div>
                        <div class="sin-metadata-value">${sinTitle}</div>
                    </div>
                    <div class="sin-metadata-item sin-metadata-full-width">
                        <div class="sin-metadata-label">SIN Description:</div>
                        <div class="sin-metadata-value">${sinDescription}</div>
                    </div>
                    <div class="sin-metadata-section-title">Codes & Classification</div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">NAICS Code(s):</div>
                        <div class="sin-metadata-value">${naicsList}</div>
                    </div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">Product Service Code (PSC):</div>
                        <div class="sin-metadata-value">${pscCode}</div>
                    </div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">Commodity Code:</div>
                        <div class="sin-metadata-value">${commodityCode === 'B' ? 'Both Products & Services' : commodityCode === 'S' ? 'Services' : commodityCode === 'P' ? 'Products' : commodityCode}</div>
                    </div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">Maximum Order Limit:</div>
                        <div class="sin-metadata-value sin-order-limit">${formattedOrderLimit}</div>
                    </div>
                    <div class="sin-metadata-section-title">Contract Options</div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">State/Local Available:</div>
                        <div class="sin-metadata-value">${stateLocal}</div>
                    </div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">Set Aside:</div>
                        <div class="sin-metadata-value">${setAside}</div>
                    </div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">Trade Discounts/Rebates (TDR):</div>
                        <div class="sin-metadata-value">${tdr}</div>
                    </div>
                    <div class="sin-metadata-item">
                        <div class="sin-metadata-label">Order Level Materials (OLM):</div>
                        <div class="sin-metadata-value">${olm}</div>
                    </div>
                </div>
            `;
            
            sinItem.addEventListener('click', function(e) {
                // Don't trigger selection if clicking on the checkbox directly
                if (e.target.type !== 'checkbox') {
                    toggleSinSelection(sin._primary_sin);
                }
            });
            
            // Handle checkbox click separately
            const checkbox = sinItem.querySelector('.sin-checkbox');
            checkbox.addEventListener('click', function(e) {
                e.stopPropagation(); // Prevent double triggering
                toggleSinSelection(sin._primary_sin);
            });
            
            sinsList.appendChild(sinItem);
        });
    }
    
    // Toggle SIN selection
    function toggleSinSelection(sinNumber) {
        if (selectedSins.has(sinNumber)) {
            selectedSins.delete(sinNumber);
        } else {
            selectedSins.add(sinNumber);
        }
        updateSelectedSinsDisplay();
        renderSinsList(); // Re-render to update selection states
    }
    
    // Update selected SINs display
    function updateSelectedSinsDisplay() {
        const selectedSinsContainer = document.getElementById('selected-sins');
        const selectedCountSpan = document.getElementById('selected-count');
        
        selectedCountSpan.textContent = `(${selectedSins.size})`;
        
        if (selectedSins.size === 0) {
            selectedSinsContainer.innerHTML = '<div class="no-selection">No SINs selected</div>';
            return;
        }
        
        selectedSinsContainer.innerHTML = '';
        selectedSins.forEach(sinNumber => {
            const sin = sinsData.find(s => s._primary_sin === sinNumber);
            if (sin) {
                const tag = document.createElement('div');
                tag.className = 'selected-sin-tag';
                tag.innerHTML = `
                    <span>${sinNumber}</span>
                    <span class="remove-sin" data-sin="${sinNumber}">×</span>
                `;
                
                tag.querySelector('.remove-sin').addEventListener('click', function(e) {
                    e.stopPropagation();
                    toggleSinSelection(sinNumber);
                });
                
                selectedSinsContainer.appendChild(tag);
            }
        });
    }
    
    // Add selected SINs to the input field
    function addSelectedSinsToField() {
        const sinsField = document.getElementById('sins_offered');
        const currentValue = sinsField.value.trim();
        const currentSins = currentValue ? currentValue.split(',').map(s => s.trim()).filter(s => s) : [];
        
        // Add new SINs that aren't already in the field
        selectedSins.forEach(sinNumber => {
            if (!currentSins.includes(sinNumber)) {
                currentSins.push(sinNumber);
            }
        });
        
        sinsField.value = currentSins.join(', ');
        
        // Close modal and clear selection
        document.getElementById('sins-modal').style.display = 'none';
        selectedSins.clear();
        updateSelectedSinsDisplay();
        
        // Auto-save the form data
        saveChecklistData(getCurrentState());
    }
    
    // SINs Modal Event Listeners
    const addSinsBtn = document.getElementById('add-sins-btn');
    const sinsModal = document.getElementById('sins-modal');
    const sinsModalCloseBtn = sinsModal.querySelector('.close-button');
    const addSelectedSinsBtn = document.getElementById('add-selected-sins-btn');
    const clearSelectionBtn = document.getElementById('clear-selection-btn');
    const sinsSearch = document.getElementById('sins-search');
    const sinsCategoryFilter = document.getElementById('sins-category-filter');
    const sinsCommodityFilter = document.getElementById('sins-commodity-filter');
    const sinsStateLocalFilter = document.getElementById('sins-state-local-filter');
    const sinsSetAsideFilter = document.getElementById('sins-set-aside-filter');
    const sinsTdrFilter = document.getElementById('sins-tdr-filter');
    const sinsOlmFilter = document.getElementById('sins-olm-filter');
    
    // Open SINs modal
    addSinsBtn.addEventListener('click', function() {
        sinsModal.style.display = 'block';
        if (sinsData.length === 0) {
            loadSinsData();
        }
    });
    
    // Close SINs modal
    sinsModalCloseBtn.addEventListener('click', function() {
        sinsModal.style.display = 'none';
        selectedSins.clear();
        updateSelectedSinsDisplay();
    });
    
    // Close modal when clicking outside
    sinsModal.addEventListener('click', function(e) {
        if (e.target === sinsModal) {
            sinsModal.style.display = 'none';
            selectedSins.clear();
            updateSelectedSinsDisplay();
        }
    });
    
    // Add selected SINs button
    addSelectedSinsBtn.addEventListener('click', addSelectedSinsToField);
    
    // Clear selection button
    clearSelectionBtn.addEventListener('click', function() {
        selectedSins.clear();
        updateSelectedSinsDisplay();
        renderSinsList();
    });
    
    // Search and filter functionality
    sinsSearch.addEventListener('input', function() {
        renderSinsList();
    });
    
    sinsCategoryFilter.addEventListener('change', function() {
        renderSinsList();
    });
    
    sinsCommodityFilter.addEventListener('change', function() {
        renderSinsList();
    });
    
    sinsStateLocalFilter.addEventListener('change', function() {
        renderSinsList();
    });
    
    sinsSetAsideFilter.addEventListener('change', function() {
        renderSinsList();
    });
    
    sinsTdrFilter.addEventListener('change', function() {
        renderSinsList();
    });
    
    sinsOlmFilter.addEventListener('change', function() {
        renderSinsList();
    });

    // Clear all filters functionality
    const clearAllFiltersBtn = document.getElementById('clear-all-filters-btn');
    clearAllFiltersBtn.addEventListener('click', function() {
        document.getElementById('sins-search').value = '';
        document.getElementById('sins-category-filter').value = '';
        document.getElementById('sins-commodity-filter').value = '';
        document.getElementById('sins-state-local-filter').value = '';
        document.getElementById('sins-set-aside-filter').value = '';
        document.getElementById('sins-tdr-filter').value = '';
        document.getElementById('sins-olm-filter').value = '';
        renderSinsList();
    });

    // Header action button event listeners
    const headerSaveBtn = document.getElementById('save-btn');
    const headerExportBtn = document.getElementById('export-btn');
    const headerImportBtn = document.getElementById('import-btn');
    const headerClearBtn = document.getElementById('clear-btn');
    const importFileInput = document.getElementById('import-file');
    
    // Manual save button
    headerSaveBtn.addEventListener('click', function() {
        const currentState = getCurrentState();
        saveChecklistData(currentState);
        
        // Visual feedback
        this.classList.add('saved');
        setTimeout(() => {
            this.classList.remove('saved');
        }, 2000);
    });
    
    // Export button
    headerExportBtn.addEventListener('click', exportData);
    
    // Import button
    headerImportBtn.addEventListener('click', function() {
        importFileInput.click();
    });
    
    // Clear button
    headerClearBtn.addEventListener('click', clearData);
    
    // File input change event
    importFileInput.addEventListener('change', importData);

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

    // Initialize core functionality after DOM is fully ready
    setTimeout(() => {
        setupAccordions();
        setupAutoSave();
        updateSectionBadges();
        
        // Load and restore saved state
        loadSavedState();
        
        // Update progress indicator
        updateProgressIndicator();
    }, 200);
});
