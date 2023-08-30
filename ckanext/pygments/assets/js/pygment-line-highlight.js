ckan.module("pygment-line-highlight", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);

            // var previewLines = document.querySelectorAll('.line');

            $(document).on('click', $('[id^="hl-line-number"]'), this._onLineClick);
            // previewLines.forEach(function (line) {
            //     line.addEventListener("click", function () {
            //         line.classList.toggle('clicked');
            //     });
            // });

            $("#hl-line-number-1").click((e) => {console.log(e)})
        },

        _onLineClick: function (e) {
            if (!e.target.text) {
                return;
            }

            let lineNumber = e.target.text.trim()

            if (isNaN(lineNumber)) {
                return;
            }

            $(".hll").toggleClass("hll");
            $("#hl-line-" + lineNumber).toggleClass("hll")
        },
    };
});
