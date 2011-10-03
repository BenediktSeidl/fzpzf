$(document).ready(function () {
    var last_executed = 0
    var last_clicked = 0

    function debug(string) {
        $("#debug").prepend("<br/>" + new Date().getTime() + " - " + string)
    }

    $("#imagesize li a").click(function () {
        var t = $(this).text()
        if (t == "0") {
            $("#image").removeAttr("width")
        } else if (t == "-") {
            $("#image").attr("width", $("#image").width() - 100)
        } else {
            $("#image").attr("width", $("#image").width() + 100)
        }
    })

    function reload_data() {
        var href = last_clicked.attr("href")
        if (href.split(".").pop() == "svg") {
            $('#image').attr("src", href + "?" + new Date().getTime())
            $('#text').hide()
            $('.image').show()
        } else {
            $('#text').text($.ajax({
                url: href,
                async: false
            }).responseText)
            $('.image').hide()
            $('#text').show()
        }
    }

    function set_text_size() {
        $("#data_container").width(0)
        $("#data_container").height(0)
        var ff = $("#fieldset_files")
        var fd = $("#fieldset_data")
        $("#fieldset_data").height(ff.height())
        $("#fieldset_data").width($("#top").width() - ff.outerWidth(true) - (fd.outerWidth(true) - fd.width()))
        $("#data_container").width($("#fieldset_data").width())
        $("#data_container").height($("#files").height())
    }

    function poll() {
        $.ajax({
            url: "/poll",
            dataType: "json",
            success: poll_success,
            error: poll_error
        })
    }

    function poll_success(data) {
        if (data['executed']) {
            debug("polling: executed")
            $("#stderr").text(data['stderr'])
            $("#stdout").text(data['stdout'])
            last_executed = new Date().getTime()
            reload_data()
            set_text_size()
            reload_files()
            changeTime()
        } else {
            debug("polling: idle")
        }
        poll()
    }

    function poll_error(data) {
        debug("polling: error")
        poll()
    }

    function changeTime() {
        $("#time").text(Math.floor((new Date().getTime() - last_executed) / 1000))
    }

    function reload_files() {
        $.ajax({
            url: "/files",
            dataType: "json",
            success: function (data) {
                var last_clicked_filename = 0
                var to_highlight = 0;
                if (last_clicked != 0){
                    last_clicked_filename = last_clicked.text()
                }
                $("#files").empty()
                for (var num in data) {
                    var file = data[num]
                    $("#files").append("<li><a href='file/" + file + "'>" + file + "</a></li>")
                    if (file == last_clicked_filename){
                        last_clicked = $("#files li a").last()
                        last_clicked.addClass("highlight")
                    }
                }
                set_text_size()
                $("#files li a").click(function () {
                    last_clicked.removeClass("highlight")
                    last_clicked = $(this)
                    last_clicked.addClass("highlight")
                    reload_data()
                    return false
                })
                if (last_clicked == 0) {
                    last_clicked = $("#file li la").last()
                    $("#files li a").last().click()
                }
            }
        })
    }

    setInterval(changeTime, 2000)
    changeTime()
    $(window).resize(set_text_size)
    poll()
    reload_files()

})
