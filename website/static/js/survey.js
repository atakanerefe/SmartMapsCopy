// // survey.js

// // Global responses object to be accessed in other files if needed
// window.responses = {};

// document.addEventListener('DOMContentLoaded', () => {
//     const submitBtn = document.querySelector('.submit-btn');

//     submitBtn.addEventListener('click', async () => {
//         const loadingSpinner = document.getElementById('loading-spinner');
//         const cardContainer = document.querySelector('.card-container');

//         loadingSpinner.classList.remove('hidden');

//         const destinationInput = document.getElementById('step-destination') || document.getElementById('summary-location');
//         const destination = destinationInput?.value.trim() || "";

//         const startDate = document.getElementById('start-date').value;
//         const endDate = document.getElementById('end-date').value;
//         const startTime = document.getElementById('start-time').value;
//         const endTime = document.getElementById('end-time').value;
//         const notes = document.getElementById('user-notes')?.value || "";

//         const environment = document.querySelector('.choice-btn[data-env].active')?.dataset.env || "Any";
//         const budget = document.querySelector('.choice-btn[data-budget].active')?.dataset.budget || "Any";
//         const vibe = document.querySelector('.choice-btn[data-choice].active')?.dataset.choice || "Any";
//         const diet = document.querySelector('.choice-btn[data-diet].active')?.dataset.diet || "None";

//         window.responses = {
//             destination,
//             startDate: startDate || null,
//             endDate: endDate || null,
//             startTime: startTime || null,
//             endTime: endTime || null,
//             environment,
//             budget,
//             vibe,
//             diet,
//             notes
//         };

//         document.getElementById('summary-location').value = destination;
//         document.getElementById('summary-date').value = startDate;
//         document.getElementById('summary-time').textContent =
//             startTime && endTime ? `${startTime} – ${endTime}` : 'Not specified';

//         try {
//             const response = await fetch("/submit_survey", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify(window.responses)
//             });

//             const data = await response.json();
//             console.log("Received cards:", data.cards);

//             cardContainer.innerHTML = "";

//             data.cards.forEach(item => {
//                 const cardEl = document.createElement("div");
//                 cardEl.className = "card";
//                 cardEl.innerHTML = `
//                     <img src="${item.image}" alt="Image of ${item.location}" class="card-image" />
//                     <div class="card-content">
//                         <div class="card-top">
//                             <h2 class="location">${item.location}</h2>
//                             <label class="select-wrapper">
//                                 <input type="checkbox" name="select_${item.location}">
//                                 <span class="select-label">Select</span>
//                             </label>
//                         </div>
//                         <div class="rating">
//                             ${"⭐".repeat(item.stars || 0)}
//                         </div>
//                         <div class="tags">
//                             ${item.tags.map(tag => `<span class="tag">${tag}</span>`).join("")}
//                         </div>
//                         <p class="description">${item.description}</p>
//                     </div>
//                 `;
//                 cardContainer.appendChild(cardEl);
//             });

//             loadingSpinner.classList.add('hidden');
//         } catch (err) {
//             loadingSpinner.classList.add('hidden');
//             console.error("Error fetching cards:", err);
//         }
//     });
// });
