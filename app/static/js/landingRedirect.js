const stayLoggedIn = localStorage.getItem('squawker-stay-logged-in');
const stayLoggedInToken = localStorage.getItem('squawker-stay-logged-in-token');
if (stayLoggedIn && stayLoggedInToken) {
    window.location.replace(`${window.location.href}is_logged_in/${stayLoggedIn}/${stayLoggedInToken}`);
} else {
    window.location.replace(`${window.location.href}login`);
}