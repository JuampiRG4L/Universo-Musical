/*
  buttons.js
  Comportamiento de los botones "Ver más" (includes/cards/artist_card.html,
  includes/cards/album_card.html). El HTML solo trae la clase .btn-ver-mas
  y un atributo data-href con el destino; este archivo es el único que
  decide qué pasa al hacer click.
*/

export function initVerMasButtons() {

    document
        .querySelectorAll(".btn-ver-mas[data-href]")
        .forEach((button) => {

            button.addEventListener("click", () => {
                window.location.href = button.dataset.href;
            });

        });

}
