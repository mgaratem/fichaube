var Pregunta = {
    // Valida el rut con su cadena completa "XXXXXXXX-X" con puntos o sin puntos
    agregaPregunta : function (){
        return true;
    }
}


$(document).ready(function(){

	$(document).on("click", ".btn-adding-row", function() {
        var row = $(".pregunta").eq(0).clone().show();
        $(".element-wrapper").append(row);

    });

    $(document).on("click", ".btn-remove-row", function() {
        var index = $(".btn-remove-row").index(this);
        $(".pregunta").eq(index).remove();
    });

});