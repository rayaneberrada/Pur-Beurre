$(function() {

	$('svg[class="svg-inline--fa fa-save fa-w-14"]').click( function(event) {
		var element_clicked = $(this).parent();
		var msg_display = $(this).next();
		$("span").remove(".message");
		console.log(element_clicked);	
		var img = element_clicked[0]["firstElementChild"]['firstChild']["currentSrc"];
		var grade = element_clicked[0]["childNodes"][3]["firstElementChild"]["currentSrc"];
		var text = element_clicked[0]["childNodes"][4]["nextSibling"].innerText;
		var code = element_clicked[0]["childNodes"][7]['innerText'];
		var url = element_clicked[0]["childNodes"][14]['previousElementSibling']['innerText'];
		console.log(img, grade, text, code, url)
		$.ajax({
			data : {
				'img' : img,
				'text' : text,
				'grade' : grade,
				'code' : code,
				'url' : url
			},
			type : 'POST',
			url : '/add_favorite/'
		})
		.done(function(data) {
			if (data.msg) {
				msg_display.after("<span class='message'>".concat(data.msg).concat("</span>"))
			}
			else {
				
			}

		});

	});

});