$(function() {

	$('svg[class="svg-inline--fa fa-save fa-w-14"]').click( function(event) {
		var element_clicked = $(this).parent();
		var msg_display = $(this).next();
		$("span").remove(".message")	
		var img = element_clicked[0]["childNodes"][1]["firstElementChild"].getAttribute("src");
		var grade = element_clicked[0]["childNodes"][1]["lastElementChild"].getAttribute("src");
		var text = element_clicked[0]["childNodes"][3].innerText;
		var code = element_clicked[0]["childNodes"][5]['innerText'];
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
			console.log(data.msg)
			console.log(msg_display)
			if (data.msg) {
				msg_display.after("<span class='message'>".concat(data.msg).concat("</span>"))
			}
			else {
				
			}

		});

	});

});