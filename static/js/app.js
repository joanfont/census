jQuery(document).ready(function($){

    var $table = $("#result");
    var $errors = $("#errors");
    var $nif = $("#nif");
    $("#cens").submit(function(evt){

        $table.hide();
        $errors.hide();

        var nif = $nif.val();

        evt.preventDefault();

        $.ajax('/find', {
            'data': {'nif': nif},
            'success': function(response, stauts, jqXHR){

                var districte = response.district;
                var seccio = response.section;
                var mesa = response.table;
                var colegi = response.school;
                var direccio = response.address;

                $("#district").html(districte);
                $("#section").html(seccio);
                $("#table").html(mesa);
                $("#school").html(colegi);
                $("#address").html(direccio);

                $table.show();

            },
            error: function(jqXHR, textStatus, errorThrown) {
                var error = $.parseJSON(jqXHR.responseText);
                $("#error").html(error.error_desc);
                $errors.show();
            },

        });

    });


    $("#delete").on('click', function(ev){
        ev.preventDefault();
        $table.hide();
        $nif.val('')
    });

});