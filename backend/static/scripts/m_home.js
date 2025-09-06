
  const successCard = document.getElementById('success-card');
  if (successCard) {
    setTimeout(() => {
      successCard.style.opacity = '0';
      successCard.style.transform = 'translateY(-20px)';
      setTimeout(() => {
        successCard.remove();
      }, 500); 
    }, 3000); 
  }

