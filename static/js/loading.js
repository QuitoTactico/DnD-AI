function loading(text, href, form) {
    text = text || "Loading";                       // Si 'text' no se proporciona, se usará "Loading" por defecto
    form = document.getElementById(form) || null;   // Si 'form' no se proporciona, se usará 'null' por defecto
    href = href || "game";                          // Si 'href' no se proporciona, se usará 'game' por defecto

    if(form == null || form.checkValidity()){
        var overlay = document.getElementById('overlay');
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