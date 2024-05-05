document.addEventListener('DOMContentLoaded', function() {
    // Retrasa la ejecución del código hasta que se haya completado el renderizado del texto
    setTimeout(function() {
        // Obtén todos los elementos con la clase 'text_animation'
        var elements = document.getElementsByClassName('text_animation');

        // Itera sobre cada elemento
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];

            // Comprueba si el texto está desbordando su contenedor
            if (element.offsetWidth < element.scrollWidth) {
                // Si el texto está desbordando, añade la clase 'animate' al elemento
                element.classList.add('animate');
            }
        }
    }, 0);  // Retrasa la ejecución del código en 0 milisegundos
});