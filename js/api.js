const API_BASE = "/api";

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
  return res.json();
}

const PokemonAPI = {
  listAll:       ()   => apiFetch("/pokemon"),
  getById:       (id) => apiFetch(`/pokemon/${id}`),
  create:        (data) => apiFetch("/pokemon", { method: "POST", body: JSON.stringify(data) }),
  getCollection: ()   => apiFetch("/collection"),
  catch:         (id) => apiFetch(`/collection/catch/${id}`, { method: "POST" }),
  release:       (id) => apiFetch(`/collection/release/${id}`, { method: "DELETE" }),
};
