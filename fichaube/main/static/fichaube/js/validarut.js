var Fn = {
    // Valida el rut con su cadena completa "XXXXXXXX-X" con puntos o sin puntos
    validaRut : function (rutCompleto) {
        rutCompleto = rutCompleto.replace('-', '-');
        if (!/^0*(\d{1,3}(\.?\d{3})*)\-([\dkK])$/.test( rutCompleto )) {
            return false;
        }

        var res = rutCompleto.replace(/\./g, '');
        var tmp = res.split('-');
        var digv = tmp[1];
        var rut = tmp[0];
        if ( digv == 'K' ){
             digv = 'k' ;
        }

        return (Fn.dv(rut) == digv );
    },
    dv : function(T){
        var M=0,S=1;
        for(;T;T=Math.floor(T/10))
            S=(S+T%10*(9-M++%6))%11;
        return S?S-1:'k';
    }
}


$(document).ready(function(){
	$("#inputRut").blur(function(){
    if (Fn.validaRut( $("#inputRut").val() )){
        $("#msgRut").html("Rut válido");
        var boton = document.getElementById("botonRegistrarse");
        boton.removeAttribute("disabled");
    } else {
        $("#msgRut").html("Rut no es válido");
    }
});
});
