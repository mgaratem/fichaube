function CheckDocumento(val){
  var div_rut = document.getElementById('groupRut');
  var input_rut = document.getElementById('inputRut');
  var div_pasaporte = document.getElementById('groupPasaporte');
  var input_pasaporte = document.getElementById('inputPasaporte');

  var valu = document.menuForm.inputTipoDocumento.options[document.menuForm.inputTipoDocumento.selectedIndex].value;

  if(val == 'PASAPORTE'){
    div_pasaporte.style.display='block';
    input_pasaporte.disabled = false;
  }
  else{
    div_pasaporte.style.display='none';
    input_pasaporte.disabled = true;
  }

  if(val == 'CEDULA'){
    div_rut.style.display='block';
    input_rut.disabled = false;
  }
  else{
    div_rut.style.display='none';
    input_rut.disabled = true;
  }
}
