(function ($) {
    $(function () {
        // Campos da tela principal
        const type = $('#id_type'),
            radios = document.getElementsByName('type'),
            frequency = $('div.fieldBox.field-frequency'),
            number_of_parcels = $('div.fieldBox.field-number_of_parcels');

        let i, length;
        // Função para tela principal
        function toggleFrequencyAndNumberOfParcels() {
            i = 0;
            length = radios.length;
            for (; i < length; i++) {
                if (radios[i].checked) {
                    radios[i].value !== 'nor' ? frequency.show() : frequency.hide();
                    radios[i].value === 'par' ? number_of_parcels.show() : number_of_parcels.hide();
                    break;
                }
            }
        }
        // Função para tela de Inline
        function toggleFrequencyAndNumberOfParcelsI(item) {
            const frequencyI = $('#'+item.id.replace("-type", "")+'-frequency');
            const number_of_parcelsI = $('#'+item.id.replace("-type", "")+'-number_of_parcels');
            item.value !== 'nor' ? frequencyI.show() : frequencyI.hide();
            item.value === 'par' ? number_of_parcelsI.show() : number_of_parcelsI.hide();
        }

        // show/hide on load based on pervious value of type
        toggleFrequencyAndNumberOfParcels();  // Tela principal

        // Tela de Inline
        i = 0;
        const typeI = $('.field-type > select');
        length = typeI.length;
        for (; i < length; i++) {
            toggleFrequencyAndNumberOfParcelsI(typeI[i]);
        }

        // show/hide on change
        type.change(function () {  // Tela Principal
            toggleFrequencyAndNumberOfParcels();
        });
        typeI.change(function () {  // Tela de Inline
            toggleFrequencyAndNumberOfParcelsI(this);
        });
    });
})(window.jQuery);
