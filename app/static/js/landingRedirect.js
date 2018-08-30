const stayLoggedIn = localStorage.getItem('squawker-stay-logged-in');
const stayLoggedInToken = localStorage.getItem('squawker-stay-logged-in-token');
if (stayLoggedIn && stayLoggedInToken) {
    window.location.replace(`${window.location.href}is_logged_in?user_id=${stayLoggedIn}&access_token=${stayLoggedInToken}`);
} else {
    window.location.replace(`${window.location.href}login`);
}