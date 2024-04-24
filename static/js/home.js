function loading(text) {
    var overlay = document.getElementById('overlay')    
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
        window.location.href = 'campaigncreation';
    });
}