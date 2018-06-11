// https://stackoverflow.com/questions/10849432/how-to-refresh-page-if-there-is-no-user-activity-for-few-seconds-using-javascrip
function setIdle(cb, seconds) {
    var timer;
    var interval = seconds * 1000;
    function refresh() {
            clearInterval(timer);
            timer = setTimeout(cb, interval);
    };
    $(document).on('keypress click', refresh);
    refresh();
}

setIdle(function() {
    location.href = location.href;
}, 30*60);
