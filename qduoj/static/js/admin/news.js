var main_page = $('#tab-content');
var news_modify_item = $('#news-modify');
var news_list_item = main_page.find('#news-body');
var news_page = 0;
var jump_flag = 0;
var last_page = false;
var editor_modify;
function init_news_list(){
    
    news_item = main_page.find('#news-list tbody');
    
    news_modify_item.hide(); 
    news_list_item.show(); 
    up_data = {
        page : news_page,
    };
    $.ys_ajax({
      
              
        url : '/admin_oj/get_news_list/',
        data : up_data,
        type : 'GET',
        
        rt_func : function(data){
            news_item.empty();
            last_page = data.last_page;
            var news_list = data.news_list;
            for(val in news_list){
            
                var item_tr = $('<tr></tr>').addClass('text-center');
                
                var td_id = $('<td></td>').html(news_list[val].id).appendTo(item_tr);
                var td_title = $('<td></td>').html(news_list[val].title).appendTo(item_tr);
                var td_user = $('<td></td>').html(news_list[val].user__user__username).appendTo(item_tr);
                var td_visible_button = $('<button class="btn btn-primary visible"></button>').text(news_list[val].visible).attr('id', news_list[val].id);
                var td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);
                var td_modify_button = $('<button class="btn btn-primary modify"></button>').text('修改').attr('id', news_list[val].id); 
                var td_modify = $('<td></td>').append(td_modify_button).appendTo(item_tr);
                var td_delete_button = $('<button class="btn btn-primary delete"></button>').text('删除').attr('id', news_list[val].id); 
                var td_modify = $('<td></td>').append(td_delete_button).appendTo(item_tr);
                item_tr.appendTo(news_item);
            }
            
            
            if(jump_flag == 0){
                $('<div id="news_page_button"></div>').appendTo(news_list_item);
                var back_button = $('<button class="btn btn-primary back" id="ads"></button>').html('back');
                back_button.appendTo($('#news_page_button'));
                var next_button = $('<button class="btn btn-primary next" id="ads"></button>').html('next');
                next_button.appendTo($('#news_page_button'));
                jump_flag = 1;
            }
        }
    });
    
    news_item.find('tr td button.visible').unbind().click(function(){   //change !!!
        up_data = {
            news_id : $(this).attr('id'),
        };
        var button = $(this);

		$.ys_ajax({

			url: '/admin_oj/news_visible/',
			data: up_data,
			type: 'GET',

			rt_func: function (data) {

				if (data.status == 200) {
					var status = button.html();

					if (status == 'true') {

						button.html('false');
					} else {
						button.html('true');
					}
				} else {
					alert('你没有权限修改');
				}
			}
		});
    });
    
    news_item.find('tr td button.delete').unbind().click(function(){
        up_data = {
            news_id : $(this).attr('id'),
        };
        
        $.ys_ajax({
            url : '/admin_oj/news_delete/',
            data : up_data,
            type : 'GET',
            
            rt_func : function(data){
                if(data.status == 200){
                    alert("Deleted successfully");
                    init_news_list();
                }
                else{
                    alert("Something is wrong");
                    init_news_list();
                }
            }
        });
    });
    
    news_item.find('tr td button.modify').unbind().click(function(){
        KindEditor.remove('textarea[name=html-news-desc-modify]');
        editor_modify = init_editor('textarea[name=html-news-desc-modify]');
        news_list_item.hide();
        news_modify_item.show();
        var news_id = $(this).attr('id');
        up_data = {
            news_id : news_id,
        };
        $.ys_ajax({
            url : '/admin_oj/news_get/',
            data : up_data,
            type : 'GET',
            
            rt_func : function(data){
				$('#html-news-title-modify').html(data.news.title);
                editor_modify.html(data.news.description);
                $('#html-news-classify-modify').val(data.news.classify);
            }
        });
        news_modify_save(news_id);
    });
    
    news_list_item.find('button.back').unbind("click").click(function(){
        if(news_page > 0)
            news_page = news_page - 1;
        init_news_list();
        $.ys_ajax({

        });
    });
    
    news_list_item.find('button.next').unbind().click(function(){
        if(last_page == false)
            news_page = news_page + 1;
        init_news_list();
        $.ys_ajax({

        });
    });
    
}

function news_modify_save(news_id){

    var news_id = news_id;
    var title = $('#html-news-title-modify').val();
    var desc = editor_modify.html();
    var classify = $('#html-news-classify-modify').val();
    news_modify_item.find('#html-news-save-modify').unbind("click").click(function(){
        
        title = $('#html-news-title-modify').val();
        desc = editor_modify.html();
        classify = $('#html-news-classify-modify').val();
        empty_flag = 0;
        news_modify_item.find('.form-control').each(function () {
            if ($(this).val() == '') {
                $(this).parent().addClass('has-error');

                $(this).focus(function () {
                    $(this).parent().removeClass('has-error');
                    $(this).unbind();
                });
                if($(this).attr('id') != 'html-news-desc-modify'){
                    empty_flag = 1;
                }
            }
            if(desc == ''){
                empty_flag = 1;
            }
        });
        
        if(empty_flag == 1){
            alert("Required part of a null value exists!");
            return ;
        }
        up_data = {
            id : news_id,
            title : title,
            desc : desc,
            classify : classify,
        }; 
        $.ys_ajax({
            url : '/admin_oj/news_modify/',
            data : up_data,
            type : 'POST',

            rt_func : function(data){
                if(data.status == 200){
                    alert("News modify successfully");
                    init_news_list();
                }
                else{
                    alert("Something is wrong");
                }
            }
        });
    });
    
}


function init_editor(id) {

	var items = [
        'source', '|', 'undo', 'redo', '|', 'preview', 'print', 'template', 'code', 'cut', 'copy', 'paste',
        'plainpaste', 'wordpaste', '|', 'justifyleft', 'justifycenter', 'justifyright',
        'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', 'subscript',
        'superscript', 'clearhtml', 'quickformat', 'selectall', '|', 'fullscreen', '/',
        'formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
        'italic', 'underline', 'strikethrough', 'lineheight', 'removeformat', '|', 'image',
        'flash', 'media', 'insertfile', 'table', 'hr', 'emoticons', 'baidumap', 'pagebreak',
        'anchor', 'link', 'unlink', '|', 'about'
	]
	var editor = KindEditor.create(id, {
		uploadJson: '',
		fileManagerJson: '',
		allowFileManager: true,
		width: '100%',
		items : items,
	});
	return editor;
}