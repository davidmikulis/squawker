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

    static async fetch(url) {
        const response = await fetch(url);
        if (response.ok) return await response.json();
        throw new Error(response.status);
    }

    static getChosenFriends() {
        return Array.from(document.getElementById('chosen-users-container').children).map(child => child.id);
    }

    static getAvailableFriends() {
        return Array.from(document.getElementById('available-users-container').children).map(child => child.id);
    }

    static createHiddenForm(action, method) {
        const form = document.createElement('form');
        form.setAttribute('id', action+'-button-'+method);
        form.setAttribute('method', method);
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
        if (!document.getElementById('background').classList.contains('background--active')) {
            const inputName = document.getElementById('setup-users-name-input').value;
            if (!inputName) {
                alert('Flock Name must be specified.');
                return;
            }
            const form = this.createHiddenForm('save', 'post');
            this.createHiddenInput('flock_name', inputName, form);
            const chosenUsersIds = this.getChosenFriends();
            if (chosenUsersIds.length < 1) {
                alert('Must choose at least one user.');
                return;
            }
            this.createHiddenInput('procedure', 'save', form);
            this.createHiddenInput('chosen_friends', JSON.stringify(chosenUsersIds), form);
            this.createHiddenInput('available_friends', JSON.stringify(this.getAvailableFriends()), form);
            form.submit();
        }
    }

    static clearButton() {
        if (!document.getElementById('background').classList.contains('background--active')) {
            const chosenUsers = Array.from(document.getElementById('chosen-users-container').children);
            const availableColumn = document.getElementById('available-users-container');
            chosenUsers.forEach(user => availableColumn.appendChild(user));
            document.getElementById('setup-users-name-input').value = '';
        }
    }


    static async getFlockNames() {
        const user_id = localStorage.getItem('squawker-stay-logged-in');
        const access_token = localStorage.getItem('squawker-stay-logged-in-token');
        const url = `http://127.0.0.1:5000/get/flock_names?user_id=${user_id}&access_token=${access_token}`;
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (e) {
            console.error(e);
        }
    }

    static loadButton() {
        const background = document.getElementById('background');
        if (!background.classList.contains('background--active')) {
            this.getFlockNames()
            .then(data => {
                const container = document.getElementById('setup-current-flocks');
                const head = document.createElement('div');
                head.classList.add('setup-current-flocks-header');
                const headText = document.createElement('div');
                headText.classList.add('setup-current-flocks-header-text');
                head.appendChild(headText);
                headText.innerText = 'My Flocks';
                container.appendChild(head);
                data.flock_names.forEach(flock => {
                    const item = document.createElement('div');
                    item.classList.add('setup-current-flocks-item');
                    const text = document.createElement('div');
                    text.classList.add('setup-current-flocks-item-text');
                    text.innerText = flock;
                    container.appendChild(item);
                    item.appendChild(text);
                    const button = document.createElement('button');
                    button.classList.add('setup-users-actions__button', 'button-purple');
                    button.innerText = 'Edit Flock';
                    button.addEventListener('click', ButtonSubmit.confirmLoadButton.bind(ButtonSubmit));
                    button.setAttribute('id', flock);
                    item.appendChild(button);
                });
                container.classList.add('setup-current-flocks--visible');
                background.classList.add('background--active');
            });
        }
    }

    static confirmLoadButton(e) {
        const background = document.getElementById('background');
        const container = document.getElementById('setup-current-flocks');
        background.classList.remove('background--active');
        container.classList.remove('setup-current-flocks--visible');
        const form = this.createHiddenForm('edit', 'post');
        this.createHiddenInput('procedure', 'load', form);
        this.createHiddenInput('flock_name', e.currentTarget.getAttribute('id'), form);
        const allFriends = this.getChosenFriends().concat(this.getAvailableFriends())
        this.createHiddenInput('all_friends', JSON.stringify(allFriends), form)
        form.submit();
    }
    
}

const setupFlashAlertFade = () => {
    const alerts = document.getElementsByClassName('flash-alert');
    if (alerts.length > 0) {
        for (let i = 0; i < alerts.length; i++) {
            alerts[i].addEventListener('transitionend', (e) => {
                console.log(e);
                element.style.setProperty('display', 'none');
            });
            alerts[i].classList.add('flash-alert-fade-out');
        }
    }
}
 
window.onload = function() {
    const clickableProfiles = document.querySelectorAll('div.user-profile-container');
    clickableProfiles.forEach(profile => profile.addEventListener('click', toggleButton));
    ['save', 'clear', 'load'].forEach(name => 
        document.getElementById('action-button-'+name).addEventListener('click', ButtonSubmit[name+'Button'].bind(ButtonSubmit))
    );

    setupFlashAlertFade();
};