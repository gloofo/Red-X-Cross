function toast_check(text) {
    let digitalElement = document.querySelector('div#bet-msg-toast div');
    if (digitalElement) {
        if (digitalElement.textContent.trim() === text) {
            return true;
        }
    }
    return false;
}

function isFullScreen() {
    return (
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement
    );
}

function preventFullScreen() {
    if (isFullScreen()) {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}

function noFullScreen() {
    document.addEventListener('fullscreenchange', preventFullScreen);
    document.addEventListener('webkitfullscreenchange', preventFullScreen);
    document.addEventListener('mozfullscreenchange', preventFullScreen);
    document.addEventListener('MSFullscreenChange', preventFullScreen);
}

function scrollToTop() {
    window.scrollTo(0, 0);
}

function currVersion() {
    let version = document.querySelector('div.dev-version');
    return version.textContent;
}

//selenium click too slow with slow internet, improvinsing with JS clicks ;0
function bet(game){
    document.querySelector(`${game}`).click();
}