// Global variables
let currentFile = null;
let sessionId = null;

// DOM Elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const browseBtn = document.getElementById('browse-btn');
const filePreview = document.getElementById('file-preview');
const previewImage = document.getElementById('preview-image');
const fileName = document.getElementById('file-name');
const processBtn = document.getElementById('process-btn');
const cancelBtn = document.getElementById('cancel-btn');
const downloadBtn = document.getElementById('download-btn');
const processAnotherBtn = document.getElementById('process-another-btn');
const tryAgainBtn = document.getElementById('try-again-btn');

// Sections
const uploadSection = document.getElementById('upload-section');
const processingSection = document.getElementById('processing-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');
const resultImage = document.getElementById('result-image');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Browse button
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Process button
    processBtn.addEventListener('click', processDocument);
    
    // Cancel button
    cancelBtn.addEventListener('click', resetToUpload);
    
    // Download button
    downloadBtn.addEventListener('click', downloadResult);
    
    // Process another button
    processAnotherBtn.addEventListener('click', resetToUpload);
    
    // Try again button
    tryAgainBtn.addEventListener('click', resetToUpload);
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/tiff', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('Please upload a valid image file (PNG, JPG, BMP, TIFF, or WEBP)');
        return;
    }
    
    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size must be less than 16MB');
        return;
    }
    
    currentFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        fileName.textContent = file.name;
        uploadArea.style.display = 'none';
        filePreview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

async function processDocument() {
    if (!currentFile) {
        showError('No file selected');
        return;
    }
    
    console.log('Starting document processing...');

    try {
        // Step 1: Upload file
        showSection(processingSection);
        setActiveStep(1);

        const formData = new FormData();
        formData.append('file', currentFile);

        console.log('Uploading file...');
        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!uploadResponse.ok) {
            const error = await uploadResponse.json();
            throw new Error(error.error || 'Upload failed');
        }

        const uploadData = await uploadResponse.json();
        sessionId = uploadData.session_id;
        console.log('Upload successful. Session ID:', sessionId);

        // Step 2: Start animation and processing in parallel
        console.log('Starting animation and processing...');
        const animationPromise = animateProcessingSteps();

        const processPromise = fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                filename: uploadData.filename
            })
        });

        // Wait for processing to complete
        console.log('Waiting for processing to complete...');
        const processResponse = await processPromise;

        if (!processResponse.ok) {
            const error = await processResponse.json();
            throw new Error(error.error || 'Processing failed');
        }

        const processData = await processResponse.json();
        console.log('Processing complete:', processData);

        // Wait for animation to finish (if it hasn't already)
        console.log('Waiting for animation to finish...');
        await animationPromise;
        console.log('Animation complete');

        // Show results
        console.log('Calling showResults()...');
        showResults();

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}

async function animateProcessingSteps() {
    const steps = [1, 2, 3, 4];
    for (let step of steps) {
        setActiveStep(step);
        await sleep(2000); // Simulate processing time for each step
    }
}

function setActiveStep(stepNumber) {
    // Remove active class from all steps
    for (let i = 1; i <= 4; i++) {
        const step = document.getElementById(`step-${i}`);
        if (step) {
            step.classList.remove('active');
        }
    }

    // Add active class to current step
    const currentStep = document.getElementById(`step-${stepNumber}`);
    if (currentStep) {
        currentStep.classList.add('active');
    }
}

function showResults() {
    console.log('showResults called with sessionId:', sessionId);

    // Load the result image
    const imageUrl = `/preview/${sessionId}?t=${Date.now()}`;
    console.log('Loading image from:', imageUrl);
    resultImage.src = imageUrl;

    // Add load event listener to verify image loads
    resultImage.onload = () => {
        console.log('Result image loaded successfully');
    };

    resultImage.onerror = () => {
        console.error('Failed to load result image');
    };

    console.log('Switching to results section');
    showSection(resultsSection);
    console.log('Results section should now be visible');
}

async function downloadResult() {
    if (!sessionId) {
        showError('No session found');
        return;
    }

    try {
        // Trigger download
        window.location.href = `/download/${sessionId}`;

        // Clean up after a short delay
        setTimeout(async () => {
            await fetch(`/cleanup/${sessionId}`, {
                method: 'POST'
            });
        }, 2000);

    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download file');
    }
}

function resetToUpload() {
    console.log('Resetting to upload screen');

    // Clear image event handlers and use blank image to prevent errors
    if (resultImage) {
        resultImage.onerror = null;
        resultImage.onload = null;
        resultImage.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    }
    if (previewImage) {
        previewImage.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    }

    // Reset state
    currentFile = null;
    sessionId = null;
    fileInput.value = '';

    // Reset UI
    uploadArea.style.display = 'block';
    filePreview.classList.add('hidden');
    fileName.textContent = '';

    // Show upload section
    showSection(uploadSection);

    console.log('Reset complete - ready for new upload');
}

function showError(message) {
    errorMessage.textContent = message;
    showSection(errorSection);
}

function showSection(section) {
    // Hide all sections
    uploadSection.classList.remove('active');
    processingSection.classList.remove('active');
    resultsSection.classList.remove('active');
    errorSection.classList.remove('active');

    // Show target section
    section.classList.add('active');
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}