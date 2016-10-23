
$(function(){
	$('#btnSignIn').click(function(){

		var email = $('#inputEmail').val();
		var password = $('#inputPassword').val();

		if(email != '' && password != ''){ //checks that all the required fields are filled
			$('#formgroupEmail').removeClass("has-error");
			$('#formgroupPassword').removeClass("has-error");
			$.ajax({
				url: '/validateLogin',
				data: $('form').serialize(),
				type: 'POST',
				success: function(response){
					console.log(response);
				},
				error: function(error){
					console.log(error);
				}
			});

		}else{ //if not, it shows the user feedback
			if(email == ''){
				$('#formgroupEmail').addClass("has-error");

			}
			if(password == ''){
				$('#formgroupPassword').addClass("has-error");

			}
		}

	});
});
