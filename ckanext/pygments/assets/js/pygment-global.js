ckan.module("pygment-global", function ($) {
    return {
        options: {
            // This is the class that is added to the body when a request is pending
            requestPendingClass: 'pygments-request-pending',
        },
        initialize: function () {
            var self = this;

            document.body.addEventListener('htmx:configRequest', function () {
                document.body.classList.add(self.options.requestPendingClass);
            });

            document.body.addEventListener('htmx:afterRequest', function () {
                document.body.classList.remove(self.options.requestPendingClass);
            });
        },
    };
});
