/*
  main.js
  Punto de entrada global, cargado en todas las páginas desde
  templates/core/base.html. Importa y arranca los módulos de
  base/, layout/ y components/ que aplican a todo el sitio.

  El JS específico de una sola página va en pages/ y se enlaza
  aparte con {% block extra_js %} en ese template (igual que
  css/pages/ con {% block extra_css %}).
*/

import { initVerMasButtons } from "./components/buttons.js";

document.addEventListener("DOMContentLoaded", () => {
    initVerMasButtons();
});
