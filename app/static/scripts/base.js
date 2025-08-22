window.addEventListener('scroll', () => {
  const header = document.getElementById('header');
  if (window.scrollY > 200) { 
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
var btnExp = document.querySelector('#btn-exp')
var menuSite = document.querySelector('.menu-lateral')

btnExp.addEventListener('click', function (e) {
    e.stopPropagation() // não fechar ao clicar no botão
    menuSite.classList.toggle('expandir')
})

// fechar ao clicar fora do menu
document.addEventListener('click', function (e) {
    if (menuSite.classList.contains('expandir') &&
        !menuSite.contains(e.target) && 
        e.target !== btnExp) {
        menuSite.classList.remove('expandir')
    }
})