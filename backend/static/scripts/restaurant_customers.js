document.addEventListener("DOMContentLoaded", (e) => {
    const summaryCards = document.querySelectorAll('.summary-card');
    summaryCards.forEach(card => {
        const mainBody = card.querySelector('.main-body');
        const openClose = card.querySelector('.openclose');
        const viewMoreBtn = card.querySelector('.view-details');
        const viewLessBtn = card.querySelector('.view-less');
        viewLessBtn.classList.add('hidden');
        viewMoreBtn.addEventListener('click', () => {
            mainBody.style.display = "flex";  
            mainBody.style.opacity = 1;  
            openClose.classList.add('open'); 
            viewMoreBtn.classList.add('hidden'); 
            viewLessBtn.classList.remove('hidden'); 
        });
        viewLessBtn.addEventListener('click', () => {
            mainBody.style.display = "none";
            mainBody.style.opacity = 0;
            openClose.classList.remove('open'); 
            viewMoreBtn.classList.remove('hidden');  
            viewLessBtn.classList.add('hidden'); 
        });
    });
});
    