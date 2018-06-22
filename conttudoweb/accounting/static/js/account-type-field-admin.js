(function ($) {
    $(function () {
        var type = $('#id_type'),
            radios = document.getElementsByName('type'),
            frequency = $('div.field-box.field-frequency'),
            number_of_parcels = $('div.field-box.field-number_of_parcels');

        function toggleFrequencyAndNumberOfParcels() {
            for (var i = 0, length = radios.length; i < length; i++) {
                if (radios[i].checked) {
                    radios[i].value == 'rec' ? frequency.show() : frequency.hide();
                    radios[i].value == 'par' ? number_of_parcels.show() : number_of_parcels.hide();
                    break;
                }
            }
        }

        // show/hide on load based on pervious value of type
        toggleFrequencyAndNumberOfParcels();

        // show/hide on change
        type.change(function () {
            toggleFrequencyAndNumberOfParcels();
        });
    });
})(django.jQuery);