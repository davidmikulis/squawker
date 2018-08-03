const dataElement = document.getElementById('data-element');
localStorage.setItem('squawker-stay-logged-in', dataElement.getAttribute('userId'))
localStorage.setItem('squawker-stay-logged-in-token', dataElement.getAttribute('accessToken'))

if (dataElement.getAttribute('redirect') === 'timeline') {
    window.location.replace(`${window.location.origin}/t`);
} else if (dataElement.getAttribute('redirect') === 'setup') {
    window.location.replace(`${window.location.origin}/setup`);
} else {
    alert('did not work');
}