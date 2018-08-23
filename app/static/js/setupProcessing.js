// Functions

const toggleButton = (e) => {
    const available = 'available-users-container';
    const chosen = 'chosen-users-container';
    switch (e.currentTarget.parentElement.id) {
        case available:
            togglePosition(e.currentTarget, document.getElementById(chosen));
            break;
        case chosen:
            togglePosition(e.currentTarget, document.getElementById(available));
            break;
        default:
            break;
    }
}

const togglePosition = (currentElement, targetColumn) => {
    // Beginning and end positions - non mutating
    const currentRect = JSON.parse(JSON.stringify(currentElement.getBoundingClientRect()));
    const targetElement = targetColumn.childElementCount > 0 ? targetColumn.lastElementChild : targetColumn;
    const targetRect = JSON.parse(JSON.stringify(targetElement.getBoundingClientRect()));
    if (targetColumn.children.length > 0) {targetRect.top += currentRect.height;}

    // Time variables
    const moveTime = 300;
    const frameDuration = 5;
    let frame = 0;
    const maxFrames = moveTime / frameDuration;

    // Position variables
    const windowHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    const xDiff = targetRect.left - currentRect.left;
    let yDiff = targetRect.top - currentRect.top;
    yDiff = Math.min(yDiff, windowHeight + currentRect.height);
    const xInc = xDiff / maxFrames;
    const yInc = yDiff / maxFrames;
    currentElement.style.position = 'absolute';

    // Store scroll values before moving in case user scrolls during animation
    const scrollX = window.scrollX;
    const scrollY = window.scrollY;

    const intervalId = window.setInterval(moveToPosition, frameDuration);
    function moveToPosition() {
        currentElement.style.left = `${currentRect.left + scrollX + xInc*frame}px`;
        currentElement.style.top = `${currentRect.top + scrollY + yInc*frame}px`;
        frame += 1;
        if (frame % maxFrames === 0) {
            window.clearInterval(intervalId);
            targetColumn.appendChild(currentElement);
            currentElement.style.position = 'initial';
            currentElement.style.left = '';
            currentElement.style.top = '';
        }
    }
};

const getChosenUsers = () => {
    toastr.success('Flock saved.');
    return Array.from(document.getElementById('chosen-users-container').children).map(child => child.id);
};

window.onload = function() {
    const clickableProfiles = document.querySelectorAll('div.user-profile-container');
    clickableProfiles.forEach(profile => profile.addEventListener('click', toggleButton));
};