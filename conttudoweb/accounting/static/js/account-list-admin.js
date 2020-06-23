(function ($) {
    $(function () {
        // Checkbox "liquidado"
        $('td.field-liquidated input').each(function () {
            if ($(this).attr('checked')) {
                // this.disabled = "disabled";
                $(this.parentNode.parentNode).addClass('liquidated');
                // const tr = $(this.parentNode.parentNode);
                // $('td.field-liquidated_date input', tr).prop( "disabled", true );
                // $('td.field-amount input', tr).prop( "disabled", true );
                // $('td.field-expected_deposit_account select', tr).prop( "disabled", true );
            }
        });
    });
})(window.jQuery);
