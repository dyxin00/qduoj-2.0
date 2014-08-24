function init_problem_list(){
    
    main_page = $('#tab-content');
    
    problem_item = main_page.find('#problem-list tbody');
    up_data = {
        page : 0,
    }; 
    $.ys_ajax({
      
              
        url : '/admin_oj/get_problem_list/',
        data : up_data,
        type : 'GET',
        
        rt_func : function(data){
            
            var problem_list = data.problem_list;
            
            for(val in problem_list){
            
                var item_tr = $('<tr></tr>').addClass('text-center');
                
                td_id = $('<td></td>').html(problem_list[val].id).appendTo(item_tr);
                td_title = $('<td></td>').html(problem_list[val].title).appendTo(item_tr);
                td_user = $('<td></td>').html(problem_list[val].user__user__username).appendTo(item_tr);
                td_visible_button = $('<button class="btn btn-primary"></button>').html(problem_list[val].visible).attr('id', problem_list[val].id);
                td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);
                
                item_tr.appendTo(problem_item);
            }
        }
    });
    
    problem_item.find('tr td button').click(function(){
    
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
        }
        });
    
    });
    
}
$(document).ready(function(){
    
});