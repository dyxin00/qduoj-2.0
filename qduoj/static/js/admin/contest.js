
var cflag = 0;
function init_contest_list(){
	$('#contest-list #contest_list').show();
	$('#contest-list #contest_fix').hide();
	var page = 0;
    main_page = $('#tab-content');
    contest_item = main_page.find('#contest-list #contest_list tbody');
	table = main_page.find('#contest-list')
    up_data = {
        page : page,
    }; 
    $.ys_ajax({
      
              
        url : '/admin_oj/get_contest_list/',
        data : up_data,
        type : 'GET',
        
        rt_func : function(data){
            
            var contest_list = data.contest_list;

			if(data.cflag == 1){
				page = page - 1; 
			}
			contest_item.empty();
			if(data.privilege & 8 != data.privilege && cflag == 0){
				$('#contest-list #contest_list table thead tr').append('<th class="td-Visible text-center">Visible</th>').append('<th class="td-Visible text-center">修改</th>');
				cflag = 1;
			}

            for(val in contest_list){
            
                var item_tr = $('<tr></tr>').addClass('text-center');
                
                var td_id = $('<td></td>').html('<a target="_blank" href = "/contest_problem_list/?cid='+contest_list[val].id + '" >'+contest_list[val].id+'</a>').appendTo(item_tr);
                var td_title = $('<td></td>').html(contest_list[val].title).appendTo(item_tr);
                var td_user = $('<td></td>').html(contest_list[val].user__user__username).appendTo(item_tr);
					
                	var td_visible_button = $('<button class="btn btn-primary visible"></button>').text(contest_list[val].visible).attr('id', contest_list[val].id);
                	var td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);
                
					
					var td_mod_button = $('<button class="btn btn-primary contest_mod"></button>').text('修改').attr('id', contest_list[val].id);
					var td_mod = $('<td></td>').append(td_mod_button).appendTo(item_tr);

                item_tr.appendTo(contest_item);
			}
			
        }
		
    });
	contest_item.find('tr td button.contest_mod').click(function(){
		
		$('#contest-list #contest_list').hide();
		$('#contest-list #contest_fix').show();
		$('#contest-list #contest_fix #contest-problem tbody').empty();
		var main_page = $('#contest-list #contest_fix').unbind();
		var table = main_page.find('#contest-problem tbody');
		
		var id = $(this).attr('id');
		up_data = {
			id : id,
		};
		$.ys_ajax({
			url : '/admin_oj/contest_get/',
			data : up_data,
			type : 'GET',
			
			rt_func : function(data){
				$('#contest_fix #id').html(data.contest.id);
				$('#contest_fix #title').html(data.contest.title);
				$('#contest_fix #desc').html(data.contest.description);
				$('#contest_fix #openrank').html(data.contest.open_rank);
				$('#contest_fix #langmask').html(data.contest.langmask);
				if(data.contest.private == 1){
					$('#contest-fix-classify').find('option[value=1]').attr('selected', 'selected').trigger('change');;
					user_table = $('#contest_fix #fix_users');
					var user_info='';
					for(flag in data.users){
						user_info += data.users[flag].user__user__username+',';
					}
					user_table.html(user_info);
				}
				for(val in data.problems){
				//	alert(data.problems[val].title);
					var item_tr = $('<tr></tr>').addClass('text-center');
					var td_id = $('<td></td>').html('<a target="_blank" href = "/problem/?pid='+data.problems[val].problem__id + '" id='+data.problems[val].problem__id+' >'+data.problems[val].problem__id+'</a>').appendTo(item_tr);

					var td_title = $('<td></td>').html(data.problems[val].problem__title).appendTo(item_tr);

					var td_user = $('<td></td>').html(data.problems[val].problem__user__user__username).appendTo(item_tr);
					var contest_title = $('<td></td>').html($('<input type="text" class="form-control" titlt_id="contest_title" id="title"/>').val(data.problems[val].title)).appendTo(item_tr);
					var contest_num = $('<td></td>').html($('<input type="text" class="form-control" num_id="contest_num" id="num" />').val(data.problems[val].num)).appendTo(item_tr);
					var contest_score = $('<td></td>').html($('<input type="text" class="form-control" num_id="contest_score" id="score" />').val(data.problems[val].sorce)).appendTo(item_tr);
					var td_delete_button = $('<button class="btn btn-danger delete"></button>').text('Delete').attr('id', data.problems[val].id);
                	var td_delete = $('<td></td>').append(td_delete_button).appendTo(item_tr);
					item_tr.appendTo(table);
				}
			}
		});
		
		contest_fix();
	});
	
    contest_item.find('tr td button.visible').click(function(){
    
        var id = $(this).attr('id');
        var button = $(this);

        up_data = {
            id : id,
        }; 
        $.ys_ajax({
      
        url : '/admin_oj/contest_visible/',
        data : up_data,
        type : 'GET',
        
        rt_func : function(data){
           
            if(data.status == 200){
                var status = button.html();
                
                if(status == 'true'){
                    
                    button.html('false');
                }else{
                    button.html('true');
                }
            }
			else{
				
				alert('你没有权限修改');
			}
        }
        });
    });
}

function contest_fix(){
	var main_page = $('#contest-list #contest_fix');
	var table = main_page.find('#contest-problem tbody');
	
	main_page.find('#problems-add').click(function(){
		var id = main_page.find('#pro-input').val();
		
		var flag = 0;
		main_page.find('tr').each(function(){
			var p_id = $(this).find('td:eq(0) a').attr('id');
			if(p_id == id){
				flag = 1;
				return;
			}
		
		});
		if(flag == 1){
			return;
		}	
		var problem_title = "ABCDEFGHIJKLMNOPQRSTUVWXYA";
		up_data = {
			id : id,
		};
		$.ys_ajax({
			
			url : '/admin_oj/problem_get/',
			data : up_data,
			type : 'GET',
			
			rt_func : function(data){
				
				if(data.status != 200){
					alert('添加失败～');
				}
				else{
					var index = table.find('tr').length;
					var item_tr = $('<tr></tr>').addClass('text-center');
					var td_id = $('<td></td>').html('<a target="_blank" href = "/problem/?pid='+data.problem.id + '" id='+data.problem.id+' >'+data.problem.id+'</a>').appendTo(item_tr);
					var td_title = $('<td></td>').html(data.problem.title).appendTo(item_tr);
					var td_user = $('<td></td>').html(data.user).appendTo(item_tr);
					var contest_title = $('<td></td>').html($('<input type="text" class="form-control" titlt_id="contest_title" id="title"/>').val(problem_title.split('')[index])).appendTo(item_tr);
					var contest_num = $('<td></td>').html($('<input type="text" class="form-control" num_id="contest_num" id="num" />').val(index + 1)).appendTo(item_tr);
					var contest_score = $('<td></td>').html('<input type="text" class="form-control" num_id="contest_score" id="score" />').appendTo(item_tr);
					var td_delete_button = $('<button class="btn btn-danger delete"></button>').text('Delete').attr('id', data.problem.id);
                	var td_delete = $('<td></td>').append(td_delete_button).appendTo(item_tr);
					item_tr.appendTo(table);
				}
			}
		});
		
		table.find('tr td button.delete').click(function(){
			id = $(this).attr('id');
			$(this).parent().parent().remove();
		});
	});
	
	main_page.find('#contest-fix').click(function(){
		var flag = 0;
		main_page.find('.form-control').each(function(){
			if($(this).val() == '' && $(this).attr('id') != 'pro-input'){
				$(this).parent().addClass('has-error');

				$(this).focus(function(){
					$(this).parent().removeClass('has-error');
					$(this).unbind();
				});
				flag = 1;
			}
		});
		
		if(flag ==1){
			return;
		}
		var contest_problem = []
		var open_rank;
		table.find('tr').each(function(i, n){
			contest_problem[i] = {
				p_id : $(n).find("td:eq(0) a").attr("id"),
				title : $(n).find("td:eq(3) input").val(),
				num : $(n).find('td:eq(4) input').val(),
				score : $(n).find('td:eq(5) input').val(),
			}
		});
		classify = main_page.find('#contest-fix-classify').val();
		
		up_data = {
			id : main_page.find('#id').val(),
			title : main_page.find('#title').val(),
			desc : main_page.find('#desc').val(),
			start_data : main_page.find('#id_start_time_0').val(),
			start_day : main_page.find('#id_start_time_1').val(),
			end_data : main_page.find('#id_end_time_0').val(),
			end_day : main_page.find('#id_end_time_1').val(),
			contest_mode : main_page.find('#contest-mode').val(),
			contest_openrank : main_page.find('#fix_open_rank').is(":checked"),
			contest_langmask : main_page.find('#langmask').val(),
			contest_classify : main_page.find('#contest-fix-classify').val(),
			
			problems : JSON.stringify(contest_problem),
		}
		if(classify == 1){
			up_data['privilege_user'] = main_page.find('#fix_users').val();
		}
		
		$.ys_ajax({
			url : '/admin_oj/contest_fix/',
			data : up_data,
			type : 'GET',
			
			rt_func : function(data){
				if(data.status==401)
					alert('add_problem wrong');
				if(data.status==402)
					alert('add_user wrong');
				if(data.status==403)
					alert('add_contest wrong');
				if(data.status==200)
					alert('比赛添加成功～');
			}
			
		});
		
	});
}

function contest_add(){
	var main_page = $('#contest-add');
	main_page.unbind();
	var table = main_page.find('#contest-problem tbody');
	main_page.find('#problems-add').click(function(){
		var id = main_page.find('#pro-input').val();
		
		var flag = 0;
		main_page.find('tr').each(function(){
			var p_id = $(this).find('td:eq(0) a').attr('id');
			if(p_id == id){
				flag = 1;
				return;
			}
		
		});
		if(flag == 1){
			return;
		}	
		var problem_title = "ABCDEFGHIJKLMNOPQRSTUVWXYA";
		up_data = {
			id : id,
		};
		$.ys_ajax({
			
			url : '/admin_oj/problem_get/',
			data : up_data,
			type : 'GET',
			
			rt_func : function(data){
				
				if(data.status != 200){
					alert('添加失败～');
				}
				else{
					var index = table.find('tr').length;
					var item_tr = $('<tr></tr>').addClass('text-center');
					var td_id = $('<td></td>').html('<a target="_blank" href = "/problem/?pid='+data.problem.id + '" id='+data.problem.id+' >'+data.problem.id+'</a>').appendTo(item_tr);
					var td_title = $('<td></td>').html(data.problem.title).appendTo(item_tr);
					var td_user = $('<td></td>').html(data.user).appendTo(item_tr);
					var contest_title = $('<td></td>').html($('<input type="text" class="form-control" titlt_id="contest_title" id="title"/>').val(problem_title.split('')[index])).appendTo(item_tr);
					var contest_num = $('<td></td>').html($('<input type="text" class="form-control" num_id="contest_num" id="num" />').val(index + 1)).appendTo(item_tr);
					var contest_score = $('<td></td>').html('<input type="text" class="form-control" num_id="contest_score" id="score" />').appendTo(item_tr);
					var td_delete_button = $('<button class="btn btn-danger delete"></button>').text('Delete').attr('id', data.problem.id);
                	var td_delete = $('<td></td>').append(td_delete_button).appendTo(item_tr);
					item_tr.appendTo(table);
				}
			}
		});
		
		table.find('tr td button.delete').click(function(){
			id = $(this).attr('id');
			$(this).parent().parent().remove();
		});
	});	
	
	
	main_page.find('#contest-add').unbind().click(function(){
		
		var flag = 0;
		main_page.find('.form-control').each(function(){
			if($(this).val() == '' && $(this).attr('id') != 'pro-input'){
				$(this).parent().addClass('has-error');

				$(this).focus(function(){
					$(this).parent().removeClass('has-error');
					$(this).unbind();
				});
				flag = 1;
			}
		});
		
		if(flag ==1){
			return;
		}
		//alert(main_page.find('#title').val()) ;
		var contest_problem = []
		var open_rank;
		table.find('tr').each(function(i, n){
			contest_problem[i] = {
				p_id : $(n).find("td:eq(0) a").attr("id"),
				title : $(n).find("td:eq(3) input").val(),
				num : $(n).find('td:eq(4) input').val(),
				score : $(n).find('td:eq(5) input').val(),
			}
		});
		classify = main_page.find('#contest-classify').val();

		up_data = {
			title : main_page.find('#title').val(),
			desc : main_page.find('#desc').val(),
			start_data : main_page.find('#id_start_time_0').val(),
			start_day : main_page.find('#id_start_time_1').val(),
			end_data : main_page.find('#id_end_time_0').val(),
			end_day : main_page.find('#id_end_time_1').val(),
			contest_mode : main_page.find('#contest-mode').val(),
			contest_openrank : main_page.find('#fix_open_rank').is(":checked"),
			contest_langmask : main_page.find('#langmask').val(),
			contest_classify : main_page.find('#contest-classify').val(),
			
			problems : JSON.stringify(contest_problem),
		}
		
		if(classify == 1){
			up_data['privilege_user'] = main_page.find('#users').val();
		}
		
		$.ys_ajax({
			url : '/admin_oj/contest_add/',
			data : up_data,
			type : 'GET',
			
			rt_func : function(data){
				if(data.status==401)
					alert('add_problem wrong');
				if(data.status==402)
					alert('add_user wrong');
				if(data.status==403)
					alert('add_contest wrong');
				if(data.status==200)
					alert('比赛添加成功～');
			}
			
		});
	});
}
 
function contest_sim(){
	$('#contest-sim #sim-list').show();
	$('#contest-sim #contest-sim-list').hide();
	main_page = $('#tab-content');
	sim_item = main_page.find('#sim-list tbody');
	sim_item.empty();
	
	$.ys_ajax({
		
		url : '/admin_oj/get_contest_list/',
		data : {},
		type : 'GET',
		
		rt_func : function(data){
			var contest_list = data.contest_list;
			for(val in contest_list){
				
                var item_tr = $('<tr></tr>').addClass('text-center');                
                var td_id = $('<td></td>').html('<a target="_blank" href = "/contest_problem_list/?cid='+contest_list[val].id + '" >'+contest_list[val].id+'</a>').appendTo(item_tr);
                var td_title = $('<td></td>').html(contest_list[val].title).appendTo(item_tr);
				var td_sim_button = $('<button class="btn btn-primary sim">').text('Sim').attr('id', contest_list[val].id);
				var td_sim = $('<td></td>').append(td_sim_button).appendTo(item_tr);
				
				item_tr.appendTo(sim_item);
			}
		}
	});
	
	sim_item.find('tr td button.sim').click(function(){
		
		$('#contest-sim #sim-list').hide();
		$('#contest-sim #contest-sim-list').show();
		sim_table = main_page.find('#contest_sim_list tbody');
		sim_table.empty();
		id = $(this).attr("id");
		up_data = {
			id : id,
		};
		
		$.ys_ajax({
			url : '/admin_oj/get_contest_sim',
			data : up_data,
			type : 'GET',
			
			rt_func : function(data){
				
				var sim_list = data.sim;
				for(val in sim_list){
					var item_tr = $('<tr></tr>').addClass('text-center');
					var s_name = $('<td></td>').html(sim_list[val].solution__user__user__username).appendTo(item_tr);
					var s1_id = $('<td></td>').html(sim_list[val].solution__id).appendTo(item_tr);
					var s2_id = $('<td></td>').html(sim_list[val].sim_s_id).appendTo(item_tr);
					var s_sim = $('<td></td>').html(sim_list[val].sim+'%').appendTo(item_tr);
					var s_sim_button = $('<button class="btn btn-primary detail">').text('详情').attr('sid', sim_list[val].solution__id).attr('smid', sim_list[val].sim_s_id);
					var s_button = $('<td></td>').append(s_sim_button).appendTo(item_tr);
				
					item_tr.appendTo(sim_table);
				}
			}
		});
		
		sim_table.find('tr td button.detail').click(function(){
			var sid = $(this).attr('sid');
			var smid = $(this).attr('smid');
			window.open('/admin_oj/get_sim_code/?sid='+sid+'&smid='+smid);
		});
		
	});
}