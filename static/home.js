$(document).ready(function () {
    $.ajax({
        type: 'POST',
        url: '/msg',
        data: JSON.stringify({"command":"load-player"}),
        dataType: "json",
        success: function (result) {
            console.log(result)
        },
        error:function () {

        }
    })
})

function begin () {
    console.log("start")
    let but = document.getElementById('showhand-button')
    but.addEventListener('click', function (e) {
        console.log('why')
        $.ajax({
            type: 'POST',
            url: '/showhandmsg',
            data: JSON.stringify({"abc":"why"}),
            dataType: "json",
            success: function (result) {
                console.log(result)
            },
            error:function () {

            }
        })
    })
    console.log(but)
}