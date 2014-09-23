function login(){
	$('#sign_in').click(function(){
		var username = $('#username').val();
		var password = $('#password').val();

		up_data = {
			username: username,
			password: password,
		};
		$.ys_ajax({
			url: '/admin_oj/login/',
			data: up_data,
			type: 'POST',
			
			rt_func: function(data){
				if(data.status==403){
					alert('登录失败~');
				}else {
					location.href = "/admin_oj/index/";
				}
			}
		});
	});
}

$(document).ready(function(){
    login();
});