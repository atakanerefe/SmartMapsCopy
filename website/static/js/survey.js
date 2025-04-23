// survey.js

// Global responses object to be accessed in other files if needed
window.responses = {};

// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('survey-modal');
    const steps = document.querySelectorAll('.survey-step');
    const nextBtns = document.querySelectorAll('.next-btn');
    const prevBtns = document.querySelectorAll('.prev-btn');
    const choiceBtns = document.querySelectorAll('.choice-btn');
    const submitBtn = document.querySelector('.submit-btn');

    let currentStep = 0;
    modal.style.display = 'flex';

    const showStep = (index) => {
        steps.forEach((step, i) => step.classList.toggle('active', i === index));
        currentStep = index;
    };

    nextBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep === 1) {
                const destination = document.getElementById('step-destination').value.trim();
                const errorDiv = document.getElementById('error-step-2');
                if (!destination) {
                    errorDiv.textContent = "Please enter a destination.";
                    return;
                }
                errorDiv.textContent = "";
                window.responses.destination = destination;
            }

            else if (currentStep === 2) {
                const startDate = document.getElementById('start-date').value;
                const endDate = document.getElementById('end-date').value;
                const errorDiv = document.getElementById('error-step-3');

                if (startDate && endDate && new Date(endDate) < new Date(startDate)) {
                    errorDiv.textContent = "End date cannot be before start date.";
                    return;
                }

                window.responses.startDate = startDate || null;
                window.responses.endDate = endDate || null;
                errorDiv.textContent = "";
            }

            else if (currentStep === 3) {
                const startTime = document.getElementById('start-time').value;
                const endTime = document.getElementById('end-time').value;
                const errorDiv = document.getElementById('error-step-4');

                if (startTime && endTime) {
                    const startDate = window.responses.startDate || '1970-01-01';
                    const endDate = window.responses.endDate || '1970-01-01';

                    const startDateTime = new Date(`${startDate}T${startTime}`);
                    const endDateTime = new Date(`${endDate}T${endTime}`);

                    if (endDateTime < startDateTime) {
                        errorDiv.textContent = "End date cannot be before start date.";
                        return;
                    }

                    window.responses.startTime = startTime;
                    window.responses.endTime = endTime;
                } else {
                    window.responses.startTime = startTime || null;
                    window.responses.endTime = endTime || null;
                }
            }

            showStep(currentStep + 1);
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep > 0) showStep(currentStep - 1);
        });
    });

    choiceBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const dataset = btn.dataset;
            if (dataset.env) window.responses.environment = dataset.env;
            if (dataset.budget) window.responses.budget = dataset.budget;
            if (dataset.vibe) window.responses.vibe = dataset.vibe;
            if (dataset.diet) window.responses.diet = dataset.diet;
            if (dataset.choice) window.responses.style = dataset.choice;
            showStep(currentStep + 1);
        });
    });

    const closeBtn = document.querySelector('.close-modal');
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    submitBtn.addEventListener('click', () => {
        const loadingSpinner = document.getElementById('loading-spinner');
    
        // Show loading spinner immediately
        loadingSpinner.classList.remove('hidden');
    
        // Close the survey modal immediately
        modal.style.display = 'none';
    
        const notes = document.getElementById('user-notes').value.trim();
        if (notes) {
            window.responses.notes = notes;
        }
    
        const tags = document.getElementById('selected-tags');
        tags.innerHTML = '';
    
        const addTag = (text) => {
            const tag = document.createElement('span');
            tag.classList.add('tag');
            tag.textContent = text;
            tags.appendChild(tag);
        };
    
        if (window.responses.environment) addTag(window.responses.environment);
        if (window.responses.budget) addTag(window.responses.budget);
        if (window.responses.vibe) addTag(window.responses.vibe);
        if (window.responses.diet) addTag(window.responses.diet);
        if (window.responses.notes) addTag('Note added');
    
        document.getElementById('summary-location').textContent = window.responses.destination || 'Not specified';
        document.getElementById('summary-date').textContent =
            window.responses.startDate && window.responses.endDate
                ? `${window.responses.startDate} – ${window.responses.endDate}`
                : window.responses.startDate || 'Not specified';
    
        document.getElementById('summary-time').textContent =
            window.responses.startTime && window.responses.endTime
                ? `${window.responses.startTime} – ${window.responses.endTime}`
                : 'Not specified';
    
        fetch("/submit_survey", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(window.responses),
        })
        .then(res => res.json())
        .then(data => {
            const container = document.querySelector(".card-container");
            container.innerHTML = "";
    
            data.cards.forEach(card => {
                const cardHTML = `
                    <div class="card">
                        <img src="${card.image}" alt="Image of ${card.location}" class="card-image" />
                        <div class="card-content">
                            <div class="card-top">
                                <h2 class="location">${card.location}</h2>
                                <label class="select-wrapper">
                                    <input type="checkbox" name="select">
                                    <span class="select-label">Select</span>
                                </label>
                            </div>
                            <div class="rating">${"⭐".repeat(Math.round(card.stars))}</div>
                            <div class="tags">
                                ${card.tags.map(tag => `<span class="tag">${tag}</span>`).join("")}
                            </div>
                            <p class="description">${card.description}</p>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML("beforeend", cardHTML);
            });
    
            // Hide loading spinner AFTER cards load
            loadingSpinner.classList.add('hidden');
            console.log("Survey Completed:", window.responses);
        })
        .catch(err => {
            loadingSpinner.classList.add('hidden');
            console.error("Error fetching cards:", err);
        });
    });
});