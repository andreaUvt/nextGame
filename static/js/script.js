document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('start-button');
    const dropDown = document.getElementById('drop-down');
    let isAtBottom = false;

    button.addEventListener('click', () => {
        if (isAtBottom) {
            // Move button and rectangle up
            dropDown.classList.remove('visible');
            setTimeout(() => {
                dropDown.classList.add('visible'); // Slide the rectangle down after 0.5 seconds
            }, 1000); // 0.5 seconds delay
            
        } else {
            // Move button and rectangle down
            button.classList.add('bottom');
            dropDown.classList.add('visible');
        }
        isAtBottom = true; // Toggle state
    });
});
document.addEventListener('DOMContentLoaded', () => {
    // Select the sliding rectangle
    const rectangle = document.getElementById('sliding-rectangle');
    
    if (rectangle) {
        // Add the 'visible' class after a short delay to trigger the slide
        setTimeout(() => {
            rectangle.classList.add('visible');
        }, 500);  // 500ms delay before it starts sliding in
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const loadMoreButton = document.getElementById('load-more');
    const gameCardsContainer = document.getElementById('game-cards-container');

    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default link behavior

            fetch(loadMoreButton.href) // Fetch the next page
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newGames = doc.querySelectorAll('.game-card'); // Extract new games
                    const nextButton = doc.querySelector('#load-more'); // Extract next "Load More" button

                    // Append new games to the container
                    newGames.forEach(game => gameCardsContainer.appendChild(game));

                    // Update or remove the "Load More" button
                    if (nextButton) {
                        loadMoreButton.href = nextButton.href;
                    } else {
                        loadMoreButton.remove(); // No more pages to load
                    }
                })
                .catch(error => console.error('Error loading more games:', error));
        });
    }
});
