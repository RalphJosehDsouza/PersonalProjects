let currentIndex = 0;
const eventsContainer = document.querySelector('.events-container');
const events = document.querySelectorAll('.event');
const totalEvents = events.length;

function setupInfiniteScroll() {
    const firstClone = Array.from(events).slice(0, 3).map(event => event.cloneNode(true));
    const lastClone = Array.from(events).slice(-3).map(event => event.cloneNode(true));

    firstClone.forEach(clone => eventsContainer.appendChild(clone));
    lastClone.forEach(clone => eventsContainer.insertBefore(clone, eventsContainer.firstChild));

    updateCarousel(false);
}

function getCardsPerView() {
    if (window.innerWidth > 1024) return 3;
    if (window.innerWidth > 768) return 2;
    return 1;
}

function updateCarousel(animated = true) {
    const cardsPerView = getCardsPerView();
    const slideWidth = 100 / cardsPerView;
    const offset = -(currentIndex + 3) * slideWidth;

    eventsContainer.style.transition = animated ? 'transform 0.5s ease-in-out' : 'none';
    eventsContainer.style.transform = `translateX(${offset}%)`;
}

function moveCarousel(direction) {
    const cardsPerView = getCardsPerView();
    currentIndex += direction * cardsPerView;
    updateCarousel();

    if (direction > 0 && currentIndex >= totalEvents) {
        setTimeout(() => {
            eventsContainer.style.transition = 'none';
            currentIndex = 0;
            updateCarousel(false);
            setTimeout(() => {
                eventsContainer.style.transition = 'transform 0.5s ease-in-out';
            }, 50);
        }, 500);
    } else if (direction < 0 && currentIndex < 0) {
        setTimeout(() => {
            eventsContainer.style.transition = 'none';
            currentIndex = totalEvents - cardsPerView;
            updateCarousel(false);
            setTimeout(() => {
                eventsContainer.style.transition = 'transform 0.5s ease-in-out';
            }, 50);
        }, 500);
    }
}

window.addEventListener('resize', () => {
    updateCarousel(false);
});

document.addEventListener('DOMContentLoaded', () => {
    setupInfiniteScroll();
});

let autoScrollInterval;

function startAutoScroll() {
    autoScrollInterval = setInterval(() => {
        moveCarousel(1);
    }, 5000);
} // Added missing closing brace

function stopAutoScroll() {
    clearInterval(autoScrollInterval);
}

document.querySelector('.carousel').addEventListener('mouseenter', stopAutoScroll);
document.querySelector('.carousel').addEventListener('mouseleave', startAutoScroll);

startAutoScroll();

function showEventDetails(eventElement) {
    const eventDetails = document.getElementById('selected-event');
    const eventName = eventElement.querySelector('h3').innerText;
    const eventDate = eventElement.querySelector('.event-date').innerText;
    const eventLocation = eventElement.querySelector('.event-location').innerText;
    const eventDescription = eventElement.querySelector('.event-description').innerText;

    eventDetails.innerHTML = `
        <h3>${eventName}</h3>
        <p><strong>Date:</strong> ${eventDate}</p>
        <p><strong>Location:</strong> ${eventLocation}</p>
        <p>${eventDescription}</p>
        <button class="register-btn" onclick="register('${eventName}')">Register Now</button>
    `;

    document.getElementById('event').value = eventName;
    document.getElementById('event-details').scrollIntoView({ behavior: 'smooth' });
}

function register(eventName) {
    document.getElementById('event').value = eventName;
    document.getElementById('registration-form').scrollIntoView({ behavior: 'smooth' });
}

document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Registration successful for ' + document.getElementById('event').value);
    document.getElementById('registration-form').reset();
});
