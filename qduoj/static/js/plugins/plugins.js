(function ($) {
    $.ys_ajax = function (option) {
        op = {
            url: '',
            type: 'GET',
//           	type: '',
            data: {},
            async: false,
            datatype: 'json',
            err_occur: function (errno) {
                return true;
            },
            rt_func: function (data) {}
        };
        for (key in option) {
            op[key] = option[key];
        };
//        get_dict = {};
//        if (op.type == 'GET') {
//            get_dict = op.data;
//            op.data = {};
//        }
        op.success = function (data) {
            if (op.err_occur(data.status)) {
                op.rt_func(data);
            }
        }
        $.ajax({
            url: op.url,
            type: op.type,
            data: op.data,
            datatype: op.datatype,
            async: op.async,
            success: op.success,
            crossDomain: true
        });
    };

	$.unpack_get = function(url){
		dst_dict = {};
		e = url.split('/');
		last_part = e[e.length - 1];
		sp_index = last_part.indexOf('?');
		dst_dict.path = last_part.substr(0, sp_index);
		params = last_part.substr(sp_index+1);
		param_set = params.split('&');
		for (i in param_set){
			param = param_set[i];
			sp_index = param.indexOf('=');
			key = param.substr(0, sp_index);
			value = param.substr(sp_index+1);
			dst_dict[key] = value;
		}
		gvar_get = dst_dict;
	};

   $.pack_get = function(dict){
		exist='';
		rtstring='';
		dict['timenow'] = Math.round(new Date().getTime()/1000);
		for (key in dict){
			if(exist==''){
				exist='?';
				connector = '';
			}else{
				connector = '&';
			}
			rtstring=rtstring+connector+key+'='+dict[key];
		}
		rtstring = exist + rtstring;
		return rtstring;
   };

})(jQuery);

function pagination_plugin(count, func, option, rt_fun, main_page){
    
//    var pagination = $('#' + pagination);
    var each_page = 20
    var pagination = main_page.find('#pagination');
    var page_count = count % each_page ? parseInt(count / each_page) + 1 : parseInt(count / each_page); 
    if(Number(count) <= each_page){
        pagination.empty();
        return;
    }
    if(count > each_page){
        pagination.empty();
        $("<li id='l'><a href='javascript:void(0);'>&laquo;</a></li>").appendTo(pagination).click(function(){
            var page_num = pagination.find('.active').attr('id');

            if(page_num <= 1){
                return;
            }
            page_num = page_num - 1;
            pagination.find('#' + page_num).find('a').click();
        });
        
        var start_page = 1, end_page = page_count, visible_page = each_page / 2, active_page = option.page + 1;
        var flag = 0;
        
        if(active_page - visible_page > 1){
            start_page = active_page - visible_page;
        }else{
            visible_page += 0 - active_page + visible_page + 1;
        }
        
        if(active_page + visible_page < page_count){
            end_page = active_page + visible_page;
            flag = 1;
        }
        else{
            start_page -= active_page + visible_page - page_count;
            if(start_page <= 1){
                start_page = 1;
            }
        }
        if(start_page != 1){
            var page = $("<li><a href='javascript:void(0);'></a></li>");
            page.addClass('disabled');
            page.find('a').html('...');
            page.appendTo(pagination);
        }
        
        for(var i = start_page; i <= end_page; i ++){
            var page = $("<li><a href='javascript:void(0);'></a></li>");
            page.find('a').html(i);
            page.attr('id', i);
            page.appendTo(pagination);
            page.click(function(){
                if($(this).hasClass('active')){
                    return;
                }
                option.page  = $(this).find('a').html() - 1;
                func(option, {
                    rt_func: rt_fun
                });
            });
        }
        
        if(flag == 1){
            var page = $("<li><a href='javascript:void(0);'></a></li>");
            page.find('a').html('...');
            page.addClass('disabled');
            page.appendTo(pagination);
        }
        $("<li id='r'><a href='javascript:void(0);'>&raquo;</a></li>").appendTo(pagination).click(function(){
            var page_num = pagination.find('.active').attr('id');
            if(page_num >= page_count){
                return;
            }
            page_num = Number(page_num) + 1;
            pagination.find("#" + page_num).find('a').click();
        });
        
        var page_active = option.page + 1;
        if(page_active == 1){
             pagination.find('#l').addClass('disabled');
        }else if(page_active == page_count){
             var page_r = Number(page_count) + 1;
             pagination.find('#r').addClass('disabled');
        }
        pagination.find('#' + page_active).addClass('active');
        $(this).addClass('active');
    }
}

