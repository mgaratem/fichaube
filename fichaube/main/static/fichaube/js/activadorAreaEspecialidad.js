function CheckUsuario(val){
  var div_profesional = document.getElementById('groupProfesional');
  var input_profesional = document.getElementById('inputEspecialidad');

  if(val == 1){
    div_profesional.style.display='block';
    input_profesional.disabled = false;
  }
  else{
    div_profesional.style.display='none';
    input_profesional.disabled = true;
  }

}
