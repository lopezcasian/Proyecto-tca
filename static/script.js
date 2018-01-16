function iniScript(){
	//Aplicando valores iniciales
	var estado;
	$('#automatico').prop('checked', false);// Se chequea el checkbox de manual
	$('#manual').prop('checked', true);
	$("#luzNatural").text("Solo en modo automático"); //Asignando texto a cajas de valores
	$("#movimiento").text("Solo en modo automático");

	funcFocos('23','off'); //Apagando los dos focos
	funcFocos('24','off');
	
	$("#manual").click(function(){ //Al presionar el checkbox manual, se habilitan los botones
		clearInterval(intervalo);
		alert("Iniciando modo manual, los controles se habilitarán");
		$('#foco1').attr("disabled",false);
		$('#foco2').attr("disabled",false);
		funcFocos('23','off'); // Se apagan los focos
		funcFocos('24','off');
		$("#movimiento").text("Solo en modo automático");
		$("#luzNatural").text("Solo en modo automático");
		$('#automatico').prop('checked', false); // 
	});
	
	function automatico(){
			$.ajax({
				url: '/automatico', // se llama a funcion automatico de app.py
				type: 'POST',
				success: function(response){ //Se recibe respues de app.py
					resp = JSON.parse(response);
					console.log(resp);
					$("#luzNatural").text(resp['luz']);
					$("#estFoco1").text(resp['1']);
					$("#estFoco2").text(resp['2']);
					$("#movimiento").text(resp['mov']);
				},
				error: function(error){
					console.log(error);
				}
			});
	}

	var intervalo;
	$("#automatico").click(function(){ //Cuando se da click en automático se deshabilita los controles
		$('#manual').prop('checked', false);
		intervalo = setInterval(function(){automatico()}, 5000); // Se llama al intervalo
		alert("Iniciando modo automático, los controles se deshabilitarán");
		$('#foco1').attr("disabled",true);
		$('#foco2').attr("disabled",true);
		
	});

	$('#foco1').click(function(){
	    if (this.checked) {
		funcFocos('23','on');//FUncion para encender
	    }else{
		funcFocos('23','off');//FUncion para apagar
	    }
	});

	$('#foco2').click(function(){
	    if (this.checked) {
		funcFocos('24','on');
	    }else{
		funcFocos('24','off');
	    }
	});

	function funcFocos(pin,accion){
		var foco;
		if(pin == '23'){
			foco = 1;
		}else{
			foco = 2;
		}
		$.ajax({
			url: '/manual/'+ pin +'/'+ accion +'', // se llama a funcion manual de app.py, con datos como el pin y la accion
			type: 'POST',
			success: function(response){
					resp = JSON.parse(response);// Se recibe respuesta de app.py
					console.log(resp);
					$("#estFoco"+foco).text(resp['estado']);
				},
			error: function(error){
					console.log(error);
				}
		});
	}
}