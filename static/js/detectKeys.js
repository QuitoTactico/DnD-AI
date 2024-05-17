document.addEventListener('keydown', function(event) {
    const promptInput = document.getElementById('promptInput');
    const key = event.key; // "ArrowUp", "ArrowDown", "ArrowRight", or "ArrowLeft"

    if (document.activeElement === promptInput) {
        return;
    }

    let direction;
    switch (key) {
        case "ArrowUp":
        case "w":
            direction = "up";
            break;
        case "ArrowDown":
        case "s":
            direction = "down";
            break;
        case "ArrowRight":
        case "d":
            direction = "right";
            break;
        case "ArrowLeft":
        case "a":
            direction = "left";
            break;
        default:
            return; // Salir si no es una tecla de flecha o WASD
    }

    promptInput.value = "/move " + direction;

    // Activar la pantalla de carga
    loading('Loading', 'game', 'actionForm');

    // Enviar el formulario automáticamente
    document.getElementById('actionForm').submit();
});