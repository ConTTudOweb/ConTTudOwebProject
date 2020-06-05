(
    function(){
        if (typeof django !== 'undefined') {
            if (django.jQuery && django.jQuery.fn && django.jQuery.fn.select2 && django.jQuery.fn.select2.amd) {
                var e = django.jQuery.fn.select2.amd;
                return e.define("pt-br", [], function () {
                    return {
                        errorLoading: function () {
                            return "Os resultados não puderam ser carregados."
                        },
                        inputTooLong: function (e) {
                            var t = e.input.length - e.maximum, n = "Apague " + t + " caracter";
                            return t != 1 && (n += "es"), n
                        },
                        inputTooShort: function (e) {
                            var t = e.minimum - e.input.length, n = "Digite " + t + " ou mais caracteres";
                            return n
                        },
                        loadingMore: function () {
                            return "Carregando mais resultados…"
                        },
                        maximumSelected: function (e) {
                            var t = "Você só pode selecionar " + e.maximum + " ite";
                            return e.maximum == 1 ? t += "m" : t += "ns", t
                        },
                        noResults: function () {
                            return "Nenhum resultado encontrado"
                        },
                        searching: function () {
                            return "Buscando…"
                        },
                        removeAllItems: function () {
                            return "Remover todos os itens"
                        }
                    }
                }), {define: e.define, require: e.require}
            }
        }
    })();
