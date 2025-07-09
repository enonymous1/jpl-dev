document.addEventListener('DOMContentLoaded', function() {
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
        }
    });

    // Modal logic
    const checklistItems = document.querySelectorAll('.checklist-item');
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close-button');
    const checkboxes = document.querySelectorAll('.checklist-card-header input[type="checkbox"]');

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
            }
        });
    });
});
