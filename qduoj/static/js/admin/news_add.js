var page = 0;
var empty_flag = 0;
var title;
var desc;
function news_add(){
    KindEditor.remove('textarea[name=html-news-desc-content]');
    var editor = init_editor('textarea[name=html-news-desc-content]');
    main_page = $('#tab-content');
    news_item = main_page.find('#news-add');
    var classify = 0;

    news_item.find('#html-news-save').unbind("click").click(function(){
        title = news_item.find('#html-news-title').val();
        desc = editor.html();
        classify = news_item.find('#html-news-classify').val();
        
        empty_flag = 0;
        news_item.find('.form-control').each(function () {
			if ($(this).val() == '') {
				$(this).parent().addClass('has-error');

				$(this).focus(function () {
					$(this).parent().removeClass('has-error');
					$(this).unbind();
				});
                if($(this).attr('id') != 'html-news-desc'){
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
            title : title,
            desc : desc,
            classify : classify,
        }; 
        $.ys_ajax({
            url : '/admin_oj/news_add/',
            data : up_data,
            type : 'POST',
             
            rt_func : function(data){
                if(data.status == 200){
                    alert("New news added successfully");
                    $('#html-news-title').val("");
                    editor.html("");
                    $('#html-news-classify').val(0);
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