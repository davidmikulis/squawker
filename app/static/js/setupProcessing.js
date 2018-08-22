// Functions

let toggleButton = (e) => {
    const available = 'available-users-container';
    const chosen = 'chosen-users-container';
    switch (e.currentTarget.parentNode.id) {
        case available:
            document.getElementById(chosen).appendChild(e.target);
            break;
        case chosen:
            document.getElementById(available).appendChild(e.target);
            break;
        default:
            break;
    }
}

const getChosenUsers = () => {
    toastr.success('Flock saved.');
    return Array.from(document.getElementById('chosen-users-container').children).map(child => child.id);
}

const clickableProfiles = document.querySelectorAll('div.user-profile-container');

clickableProfiles.forEach(profile => profile.addEventListener('click', toggleButton(profile)));