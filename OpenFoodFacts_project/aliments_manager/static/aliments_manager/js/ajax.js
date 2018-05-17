$(function() {

	$('svg[class="svg-inline--fa fa-save fa-w-14"]').click( function(event) {
		var test = $(this).parent();
		var img = test[0]["childNodes"][1].getAttribute("src");
		var text = test[0]["childNodes"][3].innerText;
		$.ajax({
			data : {
				img : img,
				text : text 
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
				console.log(img, text)
			}

		});

	});

});