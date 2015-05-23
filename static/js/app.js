jQuery(document).ready(function($){

    $("#cens").submit(function(evt){
        var $table = $("#result");
        var $errors = $("#errors");
        $table.hide();
        $errors.hide();

        var nif = $("#nif").val();

        evt.preventDefault();

        $.ajax('/consulta', {
            'data': {'nif': nif},
            'success': function(response, stauts, jqXHR){

                var districte = response.districte;
                var seccio = response.seccio;
                var mesa = response.mesa;
                var colegi = response.colegi;
                var direccio = response.direccio;

                $("#districte").html(districte);
                $("#seccio").html(seccio);
                $("#mesa").html(mesa);
                $("#colegi").html(colegi);
                $("#direccio").html(direccio);

                $table.show();

            },
            error: function(jqXHR, textStatus, errorThrown) {
                var error = $.parseJSON(jqXHR.responseText);
                $("#error").html(error.desc);
                $errors.show();
            },

        });

    });

});