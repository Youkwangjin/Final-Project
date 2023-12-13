document.addEventListener("DOMContentLoaded", function () {
    var blendAmount = 70;
    var delay = -10;
    var windowWidth = window.innerWidth;
    var bg = document.getElementById("bg");

    document.onmousemove = function (e) {
        mouseX = Math.round(e.pageX / windowWidth * 100 - delay);

        col1 = mouseX - blendAmount;
        col2 = mouseX + blendAmount;

        bg.style.background = "linear-gradient(to right, #ffdab9 " + col1 + "%, #ffadad " + col2 + "%)";

    }
});


