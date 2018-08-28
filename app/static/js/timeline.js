let didScroll;

window.addEventListener('scroll', e => didScroll = true);

setInterval(() => {
  if (didScroll) {
    hasScrolled();
    didScroll = false;
  }
}, 100);

let lastScrollTop = 0;
const delta = 5;
const timelineHeader = document.getElementById('timeline-header');
const headerHeight = timelineHeader.scrollHeight;

function hasScrolled() {
    const st = window.scrollY;
    if (Math.abs(lastScrollTop - st) <= delta) return;
    if (st > lastScrollTop && st > headerHeight){ // Scroll Down
        timelineHeader.classList.add('timeline-header--hide-up');
    } else { // Scroll Up
        timelineHeader.classList.remove('timeline-header--hide-up');
    }
  lastScrollTop = st;
}