// static/js/tags.js
let selectedTags;

document.addEventListener('DOMContentLoaded', () => {
	selectedTags = document.getElementById('selected-tags');
	const bubbleGrid = document.getElementById('bubble-grid');

	const addTagToSelected = (tagText, bubble) => {
		if ([...selectedTags.children].some(t => t.dataset.tag === tagText)) return;

		const tag = document.createElement('span');
		tag.classList.add('tag');
		tag.dataset.tag = tagText;
		tag.innerHTML = `${tagText}<span class="remove">&times;</span>`;
		tag.querySelector('.remove').onclick = () => {
			tag.remove();
			if (bubble) bubble.classList.remove('active');
		};
		selectedTags.appendChild(tag);
	};

	const toggleBubble = (bubble) => {
		const tagText = bubble.dataset.tag;
		bubble.classList.toggle('active');
		const existingTag = [...selectedTags.children].find(tag => tag.dataset.tag === tagText);
		if (existingTag) {
			existingTag.remove();
		} else {
			addTagToSelected(tagText, bubble);
		}
	};

	bubbleGrid?.querySelectorAll('.bubble').forEach(bubble => {
		bubble.addEventListener('click', () => toggleBubble(bubble));
	});

	const customInput = document.getElementById('custom-tag');
	const addButton = document.getElementById('add-custom-tag');

	const createCustomBubble = (tagText) => {
		if (!tagText) return;

		const exists = [...document.querySelectorAll('.bubble')].some(
			b => b.dataset.tag.toLowerCase() === tagText.toLowerCase()
		);
		if (exists) return;

		const bubble = document.createElement('button');
		bubble.className = 'bubble active';
		bubble.dataset.tag = tagText;
		bubble.textContent = tagText;
		bubble.addEventListener('click', () => toggleBubble(bubble));
		bubbleGrid?.appendChild(bubble);

		addTagToSelected(tagText, bubble);
	};

	customInput?.addEventListener('keydown', (e) => {
		if (e.key === 'Enter') {
			e.preventDefault();
			createCustomBubble(customInput.value.trim());
			customInput.value = '';
		}
	});

	addButton?.addEventListener('click', () => {
		createCustomBubble(customInput.value.trim());
		customInput.value = '';
	});
});