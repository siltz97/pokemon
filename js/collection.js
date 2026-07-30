document.addEventListener("DOMContentLoaded", async () => {
  const grid = document.getElementById("collection-grid");
  const searchInput = document.getElementById("search");
  let allCaught = [];

  async function loadCollection() {
    try {
      allCaught = await PokemonAPI.getCollection();
      render(allCaught);
    } catch (err) {
      grid.innerHTML = `<p class="empty-state">Errore nel caricamento della collezione: ${err.message}</p>`;
    }
  }

  function render(list) {
    if (!list.length) {
      grid.innerHTML = `
        <div class="empty-state">
          <h2>Nessun Pokémon catturato</h2>
          <p>Torna al Pokédex e inizia a catturarli!</p>
        </div>
      `;
      return;
    }
    grid.innerHTML = list.map(p => `
      <div class="pokemon-card" data-id="${p.id}">
        <div class="numero">#${String(p.numero).padStart(3, "0")}</div>
        <img src="${p.immagine_url || ""}" alt="${p.nome}" loading="lazy" />
        <div class="nome">${p.nome}</div>
        <span class="tipo">${p.tipo}</span>
        <br />
        <button class="btn-release" data-id="${p.id}">Rilascia</button>
      </div>
    `).join("");

    grid.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        e.stopPropagation();
        const id = Number(btn.dataset.id);
        try {
          await PokemonAPI.release(id);
          await loadCollection();
        } catch (err) {
          alert(`Errore: ${err.message}`);
        }
      });
    });
  }

  searchInput.addEventListener("input", () => {
    const q = searchInput.value.toLowerCase();
    const filtered = allCaught.filter(p =>
      p.nome.toLowerCase().includes(q) ||
      p.tipo.toLowerCase().includes(q) ||
      String(p.numero).includes(q)
    );
    render(filtered);
  });

  await loadCollection();
});
