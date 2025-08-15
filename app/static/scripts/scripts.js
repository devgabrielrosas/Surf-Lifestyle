window.addEventListener('scroll', () => {
  const header = document.getElementById('header-secundario');
  if (window.scrollY > 70) { 
    header.classList.add('show');
  } else {
    header.classList.remove('show');
  }
});
