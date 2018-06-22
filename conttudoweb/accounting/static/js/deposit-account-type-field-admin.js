(function ($) {
    $(function () {
        var type = $('#id_type'),
            radios = document.getElementsByName('type'),
            bank = $('.field-bank'),
            agency_number = $('.field-agency_number'),
            account_number = $('.field-account_number');

        function toggleFields() {
            for (var i = 0, length = radios.length; i < length; i++) {
                if (radios[i].checked) {
                    if (radios[i].value == 'cur') {
                        bank.show();
                        agency_number.show();
                        account_number.show();
                    } else {
                        bank.hide();
                        agency_number.hide();
                        account_number.hide();
                    }
                    break;
                }
            }
        }

        // show/hide on load based on pervious value of type
        toggleFields();

        // show/hide on change
        type.change(function () {
            toggleFields();
        });
    });
})(django.jQuery);