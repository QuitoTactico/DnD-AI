function loading() {
    var overlay = document.getElementById('overlay')    
    var loadingText = document.getElementById('loading-popup').getElementsByTagName('p')[0];
    var dots = '';

    overlay.style.display = 'block';

    var interval =  setInterval(function() {
        dots += '.';
        loadingText.innerHTML = 'Iniciando creación de campañas' + dots;
        if (dots.length > 3){
            dots = '';
        }
    },500)

    window.addEventListener('load', function() {
        clearInterval(interval);
        overlay.style.display = 'none'
    });

    window.location.href = 'campaigncreation';
}