function refresh_captcha(obj) {
    obj.src = "/get_code/";
}

function change(){
	var changed = $('#changed').unbind();
	changed.click(function(){
		var m = $('#m').val();
		var m1 = $('#m1').val();
		var m2 = $('#m2').val();
		$('#m').val('');
		$('#m1').val('');
		$('#m2').val('');
		if(m1 != m2){
			alert('两次输入密码不一致！');
		}
		else{
			$.ajax({
				url : '/password_change/',
				type : 'POST',
				dataType : 'json',
				data : {
					'm' : m,
					'm1' : m1,
					'm2' : m2,
				},
				success : function(data){
					if(data.status == 'filed'){
						alert('修改失败~');
					}
					else{
						$.ajax({
							url : '/logout/',
							type : 'GET',
							dataType : 'json',
							data : {},
							success : function(){}
						})
						location.href = "/sign_in/";
					}
				}
			})
		}
	})
}

function check_in(){
	var check = $('#check_in').unbind();
	check.click(function(){
		$.ajax({
			url : '/check_in/',
			type : 'POST',
			dataType : 'json',
			data : {
				'check_in' : 1, 
			},
			success : function(data){
				if(data.status == 'success'){
					check.html('已签到');
					alert('签到成功～');
				}
			}
		})
	})
}
function fun_check(){
	var check = $('#check_in')
	check.click(function(){
		$.ajax({
			url : '/check_in/',
			type : 'POST',
			dataType : 'json',
			data : {},
			success : function(data){
				if(data.status == 'filed'){
					check.html('已签到');
				}
				
				if(data.status == 'success'){
					check.html('签到');
					check_in();
				}
			}
		})
	})
	$('#check_in').trigger("click");
}

function news_show(){
    var news_display = $('#table-news-show')
    news_display.ready(function(){
        $.ajax({
			url : '/admin_oj/news_show/',
			type : 'POST',
			dataType : 'json',
			data : {},
			success : function(data){
				if(data.status == 'success'){
                    $('#table-news-title').html(data.news.title);
                    $('#table-news-desc').html(data.news.description);
                }
                if(data.status == 'filed'){
                    
                }
			}
		})
    })
}

$(document).ready(function(){
	fun_check();
	change();
    news_show();
})

$(document).ajaxSend(function(event, xhr, settings) {  
    function getCookie(name) {  
        var cookieValue = null;  
        if (document.cookie && document.cookie != '') {  
            var cookies = document.cookie.split(';');  
            for (var i = 0; i < cookies.length; i++) {  
                var cookie = jQuery.trim(cookies[i]);  
                // Does this cookie string begin with the name we want?  
                if (cookie.substring(0, name.length + 1) == (name + '=')) {  
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  
                    break;  
                }  
            }  
        }  
        return cookieValue;  
    }  
    function sameOrigin(url) {  
        // url could be relative or scheme relative or absolute  
        var host = document.location.host; // host + port  
        var protocol = document.location.protocol;  
        var sr_origin = '//' + host;  
        var origin = protocol + sr_origin;  
        // Allow absolute or scheme relative URLs to same origin  
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||  
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||  
            // or any other URL that isn't scheme relative or absolute i.e relative.  
            !(/^(\/\/|http:|https:).*/.test(url));  
    }  
    function safeMethod(method) {  
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));  
    }  
  
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {  
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));  
    }  
});  