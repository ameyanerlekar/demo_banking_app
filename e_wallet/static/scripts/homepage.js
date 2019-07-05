$(document).ready(function(){
	var total = 0;
	var i = 1;
	while ($("#balance_" + i).length){
		console.log($("#balance_" + i).val())
		total = total + parseFloat($("#balance_" + i).text());
		i = i + 1;
	}
	$("#total_holdings").html(total);
})
