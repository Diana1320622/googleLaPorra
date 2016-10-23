$(function() {
    $('#btnSignUp').click(function() {
      var name = $('#inputName').val();
      var surname = $('#inputSurname').val();
      var email = $('#inputEmail').val();
      var password = $('#inputPassword').val();

      if(name != '' && surname != '' && email != '' && password != ''){
        $('#formgroupName').removeClass("has-error");
        $('#formgroupSurname').removeClass("has-error");
        $('#formgroupEmail').removeClass("has-error");
        $('#formgroupPassword').removeClass("has-error");

        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('#signUpJumbotron').html('<h1>¡Usuario creado exitosamente!</h1><h3>Ingresa a tu sesión oprimiendo el botón de</h3><h3>"Inicia sesión"</h3>')
            },
            error: function(error) {
                $('#signUpJumbotron').html('<h1>404</h1><h3>Por favor intenta de nuevo</h3>')
            }
        });

      }else{

        if(name == ''){
          $('#formgroupName').addClass("has-error");
        }
        if(surname == ''){
          $('#formgroupSurname').addClass("has-error");

        }
        if(email == ''){
          $('#formgroupEmail').addClass("has-error");

        }
        if(password == ''){
          $('#formgroupPassword').addClass("has-error");

        }

      }


    });
});
