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
