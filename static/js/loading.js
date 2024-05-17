function loading(text, href, form) {
    var overlay = document.getElementById('overlay');

    // Si el overlay ya está visible, no hacer nada
    if (overlay.style.display === 'block') {
        return;
    }

    text = text || "Loading";                       // Si 'text' no se proporciona, se usará "Loading" por defecto
    form = document.getElementById(form) || null;   // Si 'form' no se proporciona, se usará 'null' por defecto
    href = href || "game";                          // Si 'href' no se proporciona, se usará 'game' por defecto

    if(form == null || form.checkValidity()){
        var loadingText = document.getElementById('loading-popup').getElementsByTagName('p')[0];
        var dots = '';

        overlay.style.display = 'block';
        loadingText.innerHTML = text;

        var interval =  setInterval(function() {
            dots += '.';
            loadingText.innerHTML = text + dots;
            if (dots.length >= 3){
                dots = '';
            }
        },500)

        window.addEventListener('load', function() {
            clearInterval(interval);
            overlay.style.display = 'none'
            window.location.href = href;
        });
    }
}