// creo un controllo se un bottone nella pagina principale viene premuto
document.addEventListener('click', event => {
    //controllo se l'evento proviene da il bottone appartenente alla classe elimina
    if (event.target.closest('.elimina')) {
        //controllo che la funzione effettivamente parta
        console.log('ciao');

        //creo riferimenti al bottone al div contatto e al suo numero di telefono
        const button = event.target.closest('.elimina'); //trovo il bottone da eliminare e creo un riferimento
        const contatto_da_eliminare = button.closest('.contatto'); //trovo il contatto che contiene il bottone e creo un riferimento
        const numero_di_telefono = contatto_da_eliminare
            .querySelector('.numero_di_telefono')
            .textContent.trim();
        console.log(numero_di_telefono); // controllo il corretto prelievo del numero di telefono
        if(confirm("Sei sicuro di voler eliminare questo contatto?")) {
            window.pywebview.api.eliminaContatto(numero_di_telefono) //utilizzo il metodo che elimina il contatto dalla rubrica temporanea e dal csv
                .then(() => window.pywebview.api.get_contatti());//successivaente aggiorno la grafica(scomparsa di un contatto)
        }
    }
});
