$(function() {

	$('svg[class="svg-inline--fa fa-save fa-w-14"]').click( function(event) {
		var test = $(this).parent();
		console.log(test);
		var img = test[0]["childNodes"][1]["firstElementChild"].getAttribute("src");
		var grade = test[0]["childNodes"][1]["lastElementChild"].getAttribute("src");
		var text = test[0]["childNodes"][3].innerText;
		var code = test[0]["childNodes"][5]['innerText'];
		console.log(code);
		$.ajax({
			data : {
				'img' : img,
				'text' : text,
				'grade' : grade,
				'code' : code
			},
			type : 'POST',
			url : '/favorite'
		})
		.done(function(data) {
			console.log(document.getElementById("story").textContent);
			if (data.error) {
				$('#addressInput').text(data.error);
			}
			else {
				
			}

		});

	});

});