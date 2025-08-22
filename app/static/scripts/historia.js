const bios = {
  kelly: {
    nome: "Robert Kelly Slater",
    apelido: ["Hell", "Slts GOAT"],
    pais: "Estados Unidos",
    titulos: "11 Campeonatos Mundiais (1992, 1994, 1995, 1996, 1997, 1998, 2005, 2006, 2008, 2010, 2011)",
    recordes: [
      "Maior número de vitórias na carreira: 57",
      "Maior número de vitórias no WCT: 56",
      "Mais vitórias em uma temporada: 7",
      "Títulos Mundiais consecutivos: 5",
      "Maior número de vitórias no Pipe Masters: 8",
      "Maior número de vitórias consecutivas no Pipe Masters: 3",
      "Campeão Mundial mais jovem: 20 anos",
      "Campeão Mundial mais velho: 39 anos",
      "Vencedor mais velho de uma etapa: 49 anos",
      "Maior pontuação em uma bateria: 20 pontos de 20 possíveis (em duas ocasiões)"
    ]
  },

  gabriel: {
    nome: "Gabriel Medina Pinto Ferreira",
    apelido: ["Gabby", "Neto de Poseidon", "Filho do Aquaman", "Percy Jackson Brasileiro"],
    pais: "Brasil",
    titulos: "3 Campeonatos Mundiais (2014, 2018, 2021)",
    recordes: [
      "Segundo surfista a realizar o back flip, um mortal de costas",
      "Primeiro brasileiro a conquistar um título mundial de surfe",
      "Primeiro surfista a realizar um back flip em uma competição oficial",
      "Surfista brasileiro com mais vitórias em etapas do WCT"
    ]
  },

  layne: {
    nome: "Layne Beachley",
    apelido: ["Layne"],
    pais: "Austrália",
    titulos: "7 Campeonatos Mundiais (1998–2003, 2006)",
    recordes: [
      "Única surfista (homem ou mulher) a vencer 6 títulos consecutivos",
      "Primeira surfista a conquistar 7 títulos mundiais",
      "Membro do Hall da Fama do Surf desde 2006"
    ]
  }
};

// --- Transforma objeto em HTML ---
function renderBioById(id) {
  const bio = bios[id];
  if (!bio) return "<p>(Sem conteúdo ainda)</p>";

  const apelidos = bio.apelido
    ? (Array.isArray(bio.apelido) ? bio.apelido.join(", ") : bio.apelido)
    : "";

  const listaRecordes = (bio.recordes || [])
    .map((r) => `<li>${r}</li>`)
    .join("");

  return `
    <p><b>Nome completo:</b> ${bio.nome}</p>
    ${apelidos ? `<p><b>Apelido:</b> ${apelidos}</p>` : ""}
    <p><b>País:</b> ${bio.pais}</p>
    ${bio.titulos ? `<p><b>Títulos:</b> ${bio.titulos}</p>` : ""}
    ${listaRecordes ? `<p><b>Recordes:</b></p><ul>${listaRecordes}</ul>` : ""}
  `;
}

// --- Abre/fecha o card e injeta o HTML renderizado ---
function toggleCard(card) {
  const id = card.dataset.id;
  const info = card.querySelector(".info");

  // fecha outros cards abertos
  document.querySelectorAll(".surfista.aberto").forEach((c) => {
    if (c !== card) {
      c.classList.remove("aberto");
      const i = c.querySelector(".info");
      if (i) {
        i.setAttribute("aria-hidden", "true");
        i.innerHTML = "";
      }
    }
  });

  const isOpen = card.classList.contains("aberto");

  if (!isOpen) {
    info.innerHTML = renderBioById(id);
    card.classList.add("aberto");
    info.setAttribute("aria-hidden", "false");
  } else {
    card.classList.remove("aberto");
    info.setAttribute("aria-hidden", "true");
    info.innerHTML = "";
  }
}

// --- Eventos de clique (img e botão/nome) ---
document.querySelectorAll(".surfista").forEach((card) => {
  const img = card.querySelector("img");
  const nome = card.querySelector(".nome");
  img && img.addEventListener("click", () => toggleCard(card));
  nome && nome.addEventListener("click", () => toggleCard(card));
});