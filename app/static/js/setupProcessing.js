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

class ButtonSubmit {
    static getChosenUsers() {
        return Array.from(document.getElementById('chosen-users-container').children).map(child => child.id);
    }

    static getAvailableUsers() {
        return Array.from(document.getElementById('available-users-container').children).map(child => child.id);
    }


    static createHiddenForm(action) {
        const form = document.createElement('form');
        form.setAttribute('id', action+'-button-post');
        form.setAttribute('method', 'post');
        form.style.setProperty('display', 'none');
        document.body.appendChild(form);
        return form;
    }

    static createHiddenInput(name, value, form) {
        const input = document.createElement('input');
        input.setAttribute('type', 'hidden');
        input.setAttribute('name', name);
        input.setAttribute('value', value);
        form.appendChild(input);
    }

    static saveButton() {
        const form = this.createHiddenForm('save');
        const name = this.createHiddenInput('name', 'professional', form);
        const chosenFriends = this.createHiddenInput(
            'chosen_friends', JSON.stringify(this.getChosenUsers()), form);
        const availableFriends = this.createHiddenInput(
            'available_friends', JSON.stringify(this.getAvailableUsers()), form);
        form.submit();
    }

    static clearButton() {}
    static loadButton() {}
    static templateButton() {}
    
}
 
window.onload = function() {
    const clickableProfiles = document.querySelectorAll('div.user-profile-container');
    clickableProfiles.forEach(profile => profile.addEventListener('click', toggleButton));
    ['save', 'clear', 'load', 'template'].forEach(name => 
        document.getElementById('action-button-'+name).addEventListener('click', ButtonSubmit[name+'Button'].bind(ButtonSubmit))
    );
};