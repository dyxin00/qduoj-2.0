function init_contest_list(){
    
    main_page = $('#tab-content');
    
    contest_item = main_page.find('#contest-list tbody');
    up_data = {
        page : 0,
    }; 
    $.ys_ajax({
      
        url : '/admin_oj/get_contest_list/',
        data : up_data,
        type : 'GET',
        
        rt_func : function(data){
            
            var contest_list = data.contest_list;
            contest_item.empty();
            for(val in contest_list){
            
                var item_tr = $('<tr></tr>').addClass('text-center');
                
                td_id = $('<td></td>').html('<a target="_blank"  href="/contest_problem_list/?cid='+contest_list[val].id+'">'+contest_list[val].id+'</a>').appendTo(item_tr);
                td_title = $('<td></td>').html(contest_list[val].title).appendTo(item_tr);
                td_user = $('<td></td>').html(contest_list[val].user__user__username).appendTo(item_tr);
                td_visible_button = $('<button class="btn btn-primary"></button>').html(contest_list[val].visible).attr('id', contest_list[val].id);
                td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);
                
                item_tr.appendTo(contest_item);
            }
        }
    });
}