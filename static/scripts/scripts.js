window.addEventListener('scroll', () => {
  const header = document.getElementById('header-secundario');
  if (window.scrollY > 111) { 
    header.classList.add('show');
  } else {
    header.classList.remove('show');
  }
});
