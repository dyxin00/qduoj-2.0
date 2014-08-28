var page = 0;
var flag = 0;
var tflag = 0;
function init_problem_list(){
    main_page = $('#tab-content');
    problem_item = main_page.find('#problem-list tbody');
	table = main_page.find('#problem-list')
    up_data = {
        page : page,
    }; 
    $.ys_ajax({
      
              
        url : '/admin_oj/get_problem_list/',
        data : up_data,
        type : 'GET',
        
        rt_func : function(data){
            
            var problem_list = data.problem_list;

			if(data.flag == 1){
				page = page - 1; 
			}
			problem_item.empty();

			if(data.privilege & 4 != 0 && flag == 0){
				$('#problem-list table thead tr').append('<th class="td-Visible text-center">Visible</th>').append('<th class="td-Visible text-center">修改</th>');
				flag = 1;
			}

            for(val in problem_list){
            
                var item_tr = $('<tr></tr>').addClass('text-center');
                
                var td_id = $('<td></td>').html('<a target="_blank" href = "/problem/?pid='+problem_list[val].id + '" >'+problem_list[val].id+'</a>').appendTo(item_tr);
                var td_title = $('<td></td>').html(problem_list[val].title).appendTo(item_tr);
                var td_user = $('<td></td>').html(problem_list[val].user__user__username).appendTo(item_tr);
				if(data.privilege & 4 != 0){
					
                	var td_visible_button = $('<button class="btn btn-primary visible"></button>').text(problem_list[val].visible).attr('id', problem_list[val].id);
                	var td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);
                
					
					var td_mod_button = $('<button class="btn btn-primary mod"></button>').text('修改').attr('id', problem_list[val].id);
					var td_mod = $('<td></td>').append(td_mod_button).appendTo(item_tr);
				}
                item_tr.appendTo(problem_item);
            }
			if(tflag == 0){
				var td_up_button = $('<button class="btn btn-primary up"></button>').text('上翻');
				td_up_button.appendTo(table);
				var td_next_button = $('<button class="btn btn-primary next"></button>').text('下翻');
				td_next_button.appendTo(table);
				tflag = 1;
			}
			
        }
		
    });
    
	
	table.find('button.next').unbind().click(function(){
		page = page + 1;
		init_problem_list();
	})
	table.find('button.up').unbind().click(function(){
		if(page > 0)
			page = page - 1;
			init_problem_list();
	})
	
	problem_item.find('tr td button.mod').click(function(){
		main_page = $('#tab-content');
		table = main_page.find('#problem-list')
		var id = $(this).attr('id');
		up_data = {
			id : id,
		};
		$.ys_ajax({
			url : '/admin_oj/problem_get/',
			data : up_data,
			type : 'GET',
			
			rt_func : function(data){
			}
		})
	});
	
    problem_item.find('tr td button.visible').click(function(){
    
        var id = $(this).attr('id');
        var button = $(this);

        up_data = {
            id : id,
        }; 
        $.ys_ajax({
      
        url : '/admin_oj/problem_visible/',
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

function problem_add(){
	
	var main_page = $('#problem-add').unbind();
	
	var flag = 0;
	main_page.find('#submit-problem').click(function(){
		
		main_page.find('.form-control').each(function(){

			if($(this).val() == ''){
				$(this).parent().addClass('has-error');

				$(this).focus(function(){
					$(this).parent().removeClass('has-error');
					$(this).unbind();
				});
				if($(this).attr('id') != 'hint' && $(this).attr('id') != 'source')
					flag = 1;
			}
		});
		
		if(flag == 1)
			return;
		console.info(main_page.find('#title').val())
		
		up_data = {
			title: main_page.find('#title').val(),
			desc: main_page.find('#desc').val(),
			desc_input: main_page.find('#desc-input').val(),
			desc_output: main_page.find('#desc-output').val(),
			sample_input: main_page.find('#sample-input').val(),
			sample_output: main_page.find('#sample-output').val(),
			hint: main_page.find('#hint').val(),
			source: main_page.find('#source').val(),
			timelimit: main_page.find('#timelimit').val(),
			memorylimit: main_page.find('#memorylimit').val(),
			classify: main_page.find('#classify').val(),
			difficult: main_page.find('#difficult').val(),
		};
		
		$.ys_ajax({
			
			url : '/admin_oj/problem_add/',
			data : up_data,
			type : 'POST',
			
			rt_func : function(data){
				if(data.status == 200){
                	alert('添加成功');
            	}else{
				  return;
				}
        	}
			
		});
	});
}