document.addEventListener("DOMContentLoaded", async () => {
  const grid = document.getElementById("pokemon-grid");
  const searchInput = document.getElementById("search");
  const btnAdd = document.getElementById("btn-add");
  const overlay = document.getElementById("modal-overlay");
  const form = document.getElementById("add-form");
  const btnCancel = document.getElementById("btn-cancel");
  let allPokemon = [];

  btnAdd.addEventListener("click", () => overlay.classList.remove("hidden"));
  btnCancel.addEventListener("click", () => overlay.classList.add("hidden"));
  overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.classList.add("hidden"); });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
      nome: document.getElementById("field-nome").value.trim(),
      tipo: document.getElementById("field-tipo").value.trim(),
      numero: Number(document.getElementById("field-numero").value),
      immagine_url: document.getElementById("field-img").value.trim(),
    };
    try {
      await PokemonAPI.create(data);
      overlay.classList.add("hidden");
      form.reset();
      await loadPokemon();
    } catch (err) {
      alert(`Errore: ${err.message}`);
    }
  });

  async function loadPokemon() {
    try {
      allPokemon = await PokemonAPI.listAll();
      render(allPokemon);
    } catch (err) {
      grid.innerHTML = `<p class="empty-state">Errore nel caricamento dei Pokémon: ${err.message}</p>`;
    }
  }

  function render(list) {
    if (!list.length) {
      grid.innerHTML = `<p class="empty-state">Nessun Pokémon trovato</p>`;
      return;
    }
    grid.innerHTML = list.map(p => `
      <div class="pokemon-card" data-id="${p.id}">
        <div class="numero">#${String(p.numero).padStart(3, "0")}</div>
        <img src="${p.immagine_url || ""}" alt="${p.nome}" loading="lazy" />
        <div class="nome">${p.nome}</div>
        <span class="tipo">${p.tipo}</span>
        ${p.catturato ? '<span class="catturato-badge">Catturato</span>' : ""}
        <br />
        <button class="${p.catturato ? "btn-release" : "btn-catch"}" data-id="${p.id}">
          ${p.catturato ? "Rilascia" : "Cattura"}
        </button>
      </div>
    `).join("");

    grid.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        e.stopPropagation();
        const id = Number(btn.dataset.id);
        const wasCaught = btn.classList.contains("btn-release");
        try {
          if (wasCaught) {
            await PokemonAPI.release(id);
          } else {
            await PokemonAPI.catch(id);
          }
          await loadPokemon();
        } catch (err) {
          alert(`Errore: ${err.message}`);
        }
      });
    });
  }

  searchInput.addEventListener("input", () => {
    const q = searchInput.value.toLowerCase();
    const filtered = allPokemon.filter(p =>
      p.nome.toLowerCase().includes(q) ||
      p.tipo.toLowerCase().includes(q) ||
      String(p.numero).includes(q)
    );
    render(filtered);
  });

  await loadPokemon();
});
