// guestLogin.js
document.addEventListener('DOMContentLoaded', () => {
	const guestBtn = document.getElementById('guest-btn');
	const loginPopup = document.getElementById('login-popup');

	guestBtn?.addEventListener('click', () => {
		if (loginPopup) {
			loginPopup.style.display = 'none';
			localStorage.setItem('loggedIn', 'guest');
		}
	});
});