/*
window.onload = function() {
    var element = document.querySelector('.history');
    element.scrollTop = element.scrollHeight;
}
*/

window.onload = function() {
    setTimeout(function() {
        var element = document.querySelector('.history');
        element.scrollTop = element.scrollHeight;
    }, 0);
}