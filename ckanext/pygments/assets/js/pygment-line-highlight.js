ckan.module("pygment-line-highlight", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);

            $(document).on('click', $('[id^="hl-line-number"]'), this._onLineClick);
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
