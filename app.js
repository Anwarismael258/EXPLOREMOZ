"use strict";
const english = document.documentElement.lang === "en";
const t = (pt, en) => english ? en : pt;
function read(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) ?? fallback; }
  catch { return fallback; }
}
function write(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); return true; }
  catch { return false; }
}
const stored = read("exploremoz:favorites", []);
const favorites = new Set(Array.isArray(stored) ? stored : []);
const buttons = [...document.querySelectorAll("[data-save]")];
const cards = [...document.querySelectorAll("[data-id]")];
const pins = new Map([...document.querySelectorAll("[data-pin]")].map(pin => [pin.dataset.pin, pin]));
const search = document.querySelector("#search");
const province = document.querySelector("#province");
const favoriteFilter = document.querySelector("#favorites");
const filters = [...document.querySelectorAll("[data-category-filter]")];
const results = document.querySelector("#results");
const normal = value => value.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");
let category = "";
function render() {
  for (const button of buttons) {
    const saved = favorites.has(button.dataset.save);
    button.setAttribute("aria-pressed", String(saved));
    button.textContent = button.classList.contains("save") ? (saved ? "♥" : "♡") :
      (saved ? t("Remover dos favoritos", "Remove from favourites") : t("Guardar nos favoritos", "Save to favourites"));
  }
  if (!results) return;
  const query = normal(search.value.trim());
  let count = 0;
  for (const card of cards) {
    const matches = normal(card.textContent).includes(query)
      && (!category || card.dataset.category === category)
      && (!province.value || card.dataset.province === province.value)
      && (favoriteFilter.getAttribute("aria-pressed") === "false" || favorites.has(card.dataset.id));
    card.hidden = !matches;
    pins.get(card.dataset.id).hidden = !matches;
    if (matches) count++;
  }
  results.textContent = count ? t(`${count} destino(s)`, `${count} destination(s)`) : t("Nenhum destino encontrado.", "No destinations found.");
}
for (const button of buttons) button.addEventListener("click", () => {
  const id = button.dataset.save;
  if (favorites.has(id)) favorites.delete(id);
  else favorites.add(id);
  write("exploremoz:favorites", [...favorites]);
  render();
});
search?.addEventListener("input", render);
province?.addEventListener("change", render);
favoriteFilter?.addEventListener("click", () => {
  favoriteFilter.setAttribute("aria-pressed", String(favoriteFilter.getAttribute("aria-pressed") === "false"));
  render();
});
for (const filter of filters) filter.addEventListener("click", () => {
  category = filter.dataset.categoryFilter;
  for (const item of filters) item.setAttribute("aria-pressed", String(item === filter));
  render();
});
render();
const form = document.querySelector("#trip");
if (form) {
  const fields = form.elements;
  const output = document.querySelector("#trip-result");
  const download = document.querySelector("#download");
  let trip = read("exploremoz:trip", null);
  let itinerary = "";
  function show(data, persisted) {
    const name = [...fields.destination.options].find(option => option.value === data.destination)?.text;
    if (!name) return;
    itinerary = [
      `${data.origin} → ${name}`, `${data.arrival} → ${data.departure} · ${data.people} ${t("pessoa(s)", "traveller(s)")}`,
      t("Chegada · Conhecer a zona e confirmar horários.", "Arrival · Explore the area and confirm opening hours."),
      t("Durante a estadia · Consultar o guia e combinar actividades locais.", "During your stay · Read the guide and arrange local activities."),
      t("Partida · Confirmar o percurso de regresso.", "Departure · Confirm your return route.")
    ].join("\n");
    output.textContent = itinerary + (persisted ? "" : t("\nArmazenamento local indisponível.", "\nLocal storage unavailable."));
    download.hidden = false;
  }
  if (trip && typeof trip === "object") {
    for (const key of ["origin", "destination", "arrival", "departure", "people"]) {
      if (typeof trip[key] === "string") fields[key].value = trip[key];
    }
    show(trip, true);
  }
  fields.departure.addEventListener("input", () => fields.departure.setCustomValidity(""));
  fields.arrival.addEventListener("input", () => fields.departure.setCustomValidity(""));
  form.addEventListener("submit", event => {
    event.preventDefault();
    trip = Object.fromEntries(new FormData(form));
    if (trip.departure < trip.arrival) {
      fields.departure.setCustomValidity(t("A partida deve ser na data da chegada ou depois.", "Departure must be on or after arrival."));
      fields.departure.reportValidity();
      return;
    }
    show(trip, write("exploremoz:trip", trip));
  });
  download.addEventListener("click", () => {
    const url = URL.createObjectURL(new Blob([itinerary], {type: "text/plain;charset=utf-8"}));
    const link = document.createElement("a");
    link.href = url;
    link.download = "exploremoz-itinerario.txt";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
}
