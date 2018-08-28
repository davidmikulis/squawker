window.onload = () => {
    let didScroll;

    window.addEventListener('scroll', e => didScroll = true);
    
    let lastScrollTop = 0;
    const delta = 5;
    const timelineHeader = document.getElementById('timeline-header');
    const headerHeight = timelineHeader.scrollHeight;
    const hasScrolled = () => {
        const st = window.scrollY;
        if (Math.abs(lastScrollTop - st) <= delta) return;
        if (st > lastScrollTop && st > headerHeight){ // Scroll Down
            timelineHeader.classList.add('timeline-header--hide-up');
        } else { // Scroll Up
            timelineHeader.classList.remove('timeline-header--hide-up');
        }
        lastScrollTop = st;
    }

    setInterval(() => {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 100);

    const setupFlashAlertFade = () => {
        const alerts = document.getElementsByClassName('flash-alert');
        if (alerts.length > 0) {
            for (let i = 0; i < alerts.length; i++) {
                alerts[i].addEventListener('transitionend', () => element.style.setProperty('display', 'none'));
                alerts[i].classList.add('flash-alert-fade-out');
            }
        }
    }

    setupFlashAlertFade();
}