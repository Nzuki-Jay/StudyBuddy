const openBtn = document.querySelector('.open-topics');
const closeBtn = document.querySelector('.close-topics');
const topicsContainer = document.querySelector('.topics-container');

openBtn.addEventListener('click', function() {
    console.log('open')
    topicsContainer.style.left = '0'; // Corrected with quotes around '0'
});

closeBtn.addEventListener('click', function() {
    console.log('close')
    topicsContainer.style.left = '-300px'; // Corrected with quotes around '-300px'
});