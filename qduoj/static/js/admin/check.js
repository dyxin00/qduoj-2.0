function admin_check(){
	main_page = $('#tab-content');
	check_item = main_page.find('#admin_check tbody');
	up_data = {}
	$.ys_ajax({

		url: '/admin_oj/get_check_list/',
		data: up_data,
		type: 'GET',

		rt_func: function (data) {
			check_item.empty();
			var check_list = data.check_list;

			for (val in check_list) {
				var item_tr = $('<tr></tr>').addClass('text-center');
				var td_id = check_list[val].cpid;
				if(td_id.indexOf("p") >= 0){
					var id = td_id.replace("p","");
					$('<td></td>').html('<a target="_blank" href = "/problem/?pid=' + id + '">' + td_id + '</a>').appendTo(item_tr);
				}
				if(td_id.indexOf('c') >= 0){
					var id = td_id.replace("c","");
					$('<td></td>').html('<a target="_blank" href = "/contest_problem_list/?cid=' + id + '">' + td_id + '</a>').appendTo(item_tr);
				}
				$('<td></td>').html('<input type="text" class="form-control" id="check" value = '+check_list[val].check+' />').appendTo(item_tr);
				$('<td></td>').html(check_list[val].user__user__username).appendTo(item_tr);
				$('<td></td>').html('<input type="text" class="form-control" id="desc" value = '+check_list[val].desc+' />').appendTo(item_tr);
				var td_save_button = $('<button class="btn btn-success save"></button>').text('Save').attr('id', td_id);
				var td_save = $('<td></td>').append(td_save_button).appendTo(item_tr);
				item_tr.appendTo(check_item);
			}
		}
	});
	check_item.find('tr td button.save').click(function(){
		var id = this.id;
		var status = $(this).parent().parent().find('td #check').val();	
		var desc = $(this).parent().parent().find('td #desc').val();
		up_data = {
			id : id,
			check : status,
			desc : desc,
		}
		
		$.ys_ajax({
			
			url: '/admin_oj/check_save/',
			data: up_data,
			type: 'GET',
			
			rt_func: function(data){
				if(data.status == 200){
					alert('save success!');
				}
				else{
					alert('save faile!');
				}
			}
		});
	});

}