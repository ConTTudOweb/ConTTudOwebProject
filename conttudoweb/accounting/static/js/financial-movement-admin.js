(function ($) {
    $(function () {
        const td = $('.field-amount_converted');
        console.log(td);
        td.each(function() {
            const td_value = $(this).html(); //get the value
            if (parseFloat(td_value) < 0) {
                $(this).css({'color': 'red'});
            }
        });
    });
})(window.jQuery);
