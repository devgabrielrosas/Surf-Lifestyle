const bios = {
    kelly: "<p><b>Biografia:</b> CARECA QUE SURFA MUITO</p>",
    gabriel: "<p><b>Biografia:</b>BRASILEIRO QUE SURFA MUITO</p>",
    layne: "<p><b>Biografia:</b>MUIÉ QUE NAO SEI SE SURFA MUITO</p>",
};

//  Função para abrir e fechar o card
function toggleCard(card){
    const id = card.dataset.id;
    const info = card.querySelector(".info");

    // essa parte fecha todos os outros cards abertos
    document.querySelectorAll(".surfista.aberto").forEach((c) => {
        if (c !== card) c.classList.remove("aberto");
    })
    // Esse daqui preenche a bio so qundo for abrir
    if (!card.classList.contains("aberto")) {
    info.innerHTML = bios[id] || "<p>(Sem conteúdo ainda)</p>";
    card.classList.add("aberto");
    info.setAttribute("aria-hidden", "false");
  } else {
    card.classList.remove("aberto");
    info.setAttribute("aria-hidden", "true");
  }
}


// Adiciona cliques na imagem e no nome
document.querySelectorAll(".surfista").forEach((card) => {
  const img = card.querySelector("img");
  const nome = card.querySelector(".nome");

  img.addEventListener("click", () => toggleCard(card));
  nome.addEventListener("click", () => toggleCard(card));
});

