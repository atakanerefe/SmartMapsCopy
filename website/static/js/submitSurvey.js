// submitSurvey.js
document.addEventListener('DOMContentLoaded', () => {
	const surveyForm = document.querySelector('.submit-btn');
	const cardContainer = document.querySelector('.card-container');
	const loadingSpinner = document.getElementById('loading-spinner');
	const placeholderBox = document.querySelector(".card-list");

    const selectedTags = document.getElementById('selected-tags');

	surveyForm?.addEventListener('click', async () => {
		loadingSpinner.classList.remove('hidden');

		const destinationInput = document.getElementById('step-destination') || document.getElementById('summary-location');
		const destination = destinationInput?.value.trim() || "";
		const startDate = document.getElementById('start-date')?.value || null;
		const endDate = document.getElementById('end-date')?.value || null;
		const startTime = document.getElementById('start-time')?.value || null;
		const endTime = document.getElementById('end-time')?.value || null;
		const notes = document.getElementById('user-notes')?.value || "";
		const environment = document.querySelector('.choice-btn[data-env].active')?.dataset.env || "Any";
		const budget = document.querySelector('.choice-btn[data-budget].active')?.dataset.budget || "Any";
		const vibe = document.querySelector('.choice-btn[data-choice].active')?.dataset.choice || "Any";
		const diet = document.querySelector('.choice-btn[data-diet].active')?.dataset.diet || "None";
		const tags = [...selectedTags.querySelectorAll('.tag')].map(tag => tag.dataset.tag);

		const surveyData = {
			destination,
			startDate,
			endDate,
			startTime,
			endTime,
			environment,
			budget,
			vibe,
			diet,
			notes,
			tags
		};

		try {
			const response = await fetch("/submit_survey", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(surveyData)
			});

			const data = await response.json();
			console.log("Received cards:", data.cards);

			const placeholderText = document.getElementById('placeholder-message');
			if (placeholderText) {
				placeholderText.style.display = "none";
			}

			cardContainer.innerHTML = "";

			let allCards = data.cards;
			let currentPage = 1;
			const cardsPerPage = 5;

			function renderPage(page) {
				cardContainer.innerHTML = "";
				const start = (page - 1) * cardsPerPage;
				const end = start + cardsPerPage;
				const cardsToRender = allCards.slice(start, end);

				cardsToRender.forEach(item => {
					const cardEl = document.createElement("div");
					cardEl.className = "card";
					cardEl.innerHTML = `
						<img src="${item.image}" alt="Image of ${item.location}" class="card-image" />
						<div class="card-content">
							<div class="card-top">
								<h2 class="location">${item.location}</h2>
								<label class="select-wrapper">
									<input type="checkbox" name="select_${item.location}">
									<span class="select-label">Select</span>
								</label>
							</div>
							<div class="rating">${"⭐".repeat(item.stars || 0)}</div>
							<div class="tags">${item.tags.map(tag => `<span class="tag">${tag}</span>`).join("")}</div>
							<p class="description">${item.description}</p>
						</div>`;
					cardContainer.appendChild(cardEl);
				});

				document.getElementById("prev-btn").style.display = page > 1 ? "inline-block" : "none";
				document.getElementById("next-btn").style.display = end < allCards.length ? "inline-block" : "none";
			}

			document.getElementById("prev-btn").addEventListener("click", () => {
				if (currentPage > 1) {
					currentPage--;
					renderPage(currentPage);
				}
			});

			document.getElementById("next-btn").addEventListener("click", () => {
				if (currentPage * cardsPerPage < allCards.length) {
					currentPage++;
					renderPage(currentPage);
				}
			});

			renderPage(currentPage);

			const paginationControls = document.querySelector(".pagination-controls");
			paginationControls.style.display = allCards.length > cardsPerPage ? "flex" : "none";

		} catch (err) {
			console.error("Error fetching cards:", err);
		} finally {
			loadingSpinner.classList.add('hidden');
		}
	});
});