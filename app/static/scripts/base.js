window.addEventListener('scroll', () => {
  const header = document.getElementById('header');
  if (window.scrollY > 80) { 
    header.classList.add('show');
  } else {
    header.classList.remove('show');
  }
});

var menuItem = document.querySelectorAll('.item-menu')

function selectLink() {
    menuItem.forEach((item) =>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo')
}

menuItem.forEach((item) =>
    item.addEventListener('click', selectLink)
)


// expandir o menu
var btnExp = document.getElementById('btn-exp')
var btnClose = document.getElementById('btn-close')
var menuSite = document.querySelector('.menu-lateral')

btnExp.addEventListener('click', function (e) {
    e.stopPropagation() // não fechar ao clicar no botão
    menuSite.classList.toggle('expandir')
    btnExp.style.display="none"
})

// fechar ao clicar fora do menu
document.addEventListener('click', function (e) {
    if (menuSite.classList.contains('expandir') &&
        !menuSite.contains(e.target) && 
        e.target !== btnExp) {
        menuSite.classList.remove('expandir')
        setTimeout(function () {btnExp.style.display = "block"}, 300);
    }
})
document.addEventListener('click', function (e) {
    if (menuSite.classList.contains('expandir') && 
        e.target == btnClose) {
        menuSite.classList.remove('expandir')
        setTimeout(function () {btnExp.style.display = "block"}, 300);
    }
})