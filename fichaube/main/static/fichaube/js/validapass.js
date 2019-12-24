var Pw = {
    validaPass : function (pass) {
        var res = pass.split("");
        var largo = res.length

        if ( largo <= 5 ){
             return false;
        }

        else {
            return true;
        }
    },
    hola : function(){
    }
}


$(document).ready(function(){
	$("#inputPassNueva").blur(function(){
    if (Pw.validaPass( $("#inputPassNueva").val() )){
        $("#msgPass").html("Contrase&ntilde;a Válida");
        var boton = document.getElementById("botonCambiarPass");
        boton.removeAttribute("disabled");
    } else {
        $("#msgPass").html("Contrase&ntilde;a no válida");
    }
});
});
