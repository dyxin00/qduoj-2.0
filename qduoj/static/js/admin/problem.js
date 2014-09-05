var page = 0;
var flag = 0;
var tflag = 0;
var sflag = 0;
var editor_modify;
function init_problem_list() {
	main_page = $('#tab-content');

	problem_item = main_page.find('#problem-table tbody');
	table = main_page.find('#problem-table');
	$('#problem-list #problem-modify').hide();
	$('#problem-list #problem-table').show();
	$('#bt').show();
	up_data = {
		page: page,
	};
	$.ys_ajax({


		url: '/admin_oj/get_problem_list/',
		data: up_data,
		type: 'GET',

		rt_func: function (data) {

			var problem_list = data.problem_list;

			if (data.flag == 1) {
				page = page - 1;
			}
			problem_item.empty();

			if (data.privilege & 4 != data.privilege && flag == 0) {
				$('#problem-list table thead tr').append('<th class="td-Visible text-center">Visible</th>').append('<th class="td-Visible text-center">修改</th>');
				flag = 1;
			}

			for (val in problem_list) {
				var item_tr = $('<tr></tr>').addClass('text-center');

				var td_id = $('<td></td>').html('<a target="_blank" href = "/problem/?pid=' + problem_list[val].id + '" >' + problem_list[val].id + '</a>').appendTo(item_tr);
				var td_title = $('<td></td>').html(problem_list[val].title).appendTo(item_tr);
				var td_user = $('<td></td>').html(problem_list[val].user__user__username).appendTo(item_tr);
				if (data.privilege & 4 != 0) {

					var td_visible_button = $('<button class="btn btn-primary visible"></button>').text(problem_list[val].visible).attr('id', problem_list[val].id);
					var td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);


					var td_mod_button = $('<button class="btn btn-primary mod"></button>').text('修改').attr('id', problem_list[val].id);


					var td_mod = $('<td></td>').append(td_mod_button).appendTo(item_tr);
				}
				item_tr.appendTo(problem_item);
			}
			if (tflag == 0) {
				$('<div id="bt">').appendTo(table);
				var td_up_button = $('<button class="btn btn-primary back" id="ads"></button>').text('上翻');
				td_up_button.appendTo("#bt");
				var td_next_button = $('<button class="btn btn-primary next" id="ads"></button>').text('下翻');
				td_next_button.appendTo("#bt");
				tflag = 1;
			}

		}

	});


	table.find('button.next').unbind().click(function () {
		page = page + 1;
		init_problem_list();
	})
	table.find('button.back').unbind().click(function () {
		if (page > 0)
			page = page - 1;
		init_problem_list();
	})

	table.find('#serach').unbind().click(function () {
		$('#bt').hide();
		id = table.find('.form-control').val();
		up_data = {
			id: id,
		};
		$.ys_ajax({

			url: '/admin_oj/problem_get/',
			data: up_data,
			type: 'GET',

			rt_func: function (data) {
				if (data.status != 200) {
					alert("没找到～");
				} else {
					problem_item.empty();

					var item_tr = $('<tr></tr>').addClass('text-center');

					var td_id = $('<td></td>').html('<a target="_blank" href = "/problem/?pid=' + data.problem.id + '" >' + data.problem.id + '</a>').appendTo(item_tr);
					var td_title = $('<td></td>').html(data.problem.title).appendTo(item_tr);
					var td_user = $('<td></td>').html(data.user).appendTo(item_tr);
					if (data.privilege & 4 != data.privilege) {

						var td_visible_button = $('<button class="btn btn-primary visible"></button>').text(data.problem.visible).attr('id', data.problem.id);
						var td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);
						var td_mod_button = $('<button class="btn btn-primary mod"></button>').text('修改').attr('id', data.problem.id);
						var td_mod = $('<td></td>').append(td_mod_button).appendTo(item_tr);
					}
					item_tr.appendTo(problem_item);
				}
			}
		});
	});
	
	table.find('#classify').unbind().click(function () {
		classify = $(this).val();
		up_data = {

			classify: classify,
		};
		$.ys_ajax({

			url: '/admin_oj/get_problem_list/',
			data: up_data,
			type: 'GET',

			rt_func: function (data) {
				var problem_list = data.problem_list;

				if (data.flag == 1) {
					page = page - 1;
				}
				problem_item.empty();

				if (data.privilege & 4 != data.privilege && flag == 0) {
					$('#problem-list table thead tr').append('<th class="td-Visible text-center">Visible</th>').append('<th class="td-Visible text-center">修改</th>');
					flag = 1;
				}

				for (val in problem_list) {
					var item_tr = $('<tr></tr>').addClass('text-center');

					var td_id = $('<td></td>').html('<a target="_blank" href = "/problem/?pid=' + problem_list[val].id + '" >' + problem_list[val].id + '</a>').appendTo(item_tr);
					var td_title = $('<td></td>').html(problem_list[val].title).appendTo(item_tr);
					var td_user = $('<td></td>').html(problem_list[val].user__user__username).appendTo(item_tr);
					if (data.privilege & 4 != 0) {

						var td_visible_button = $('<button class="btn btn-primary visible"></button>').text(problem_list[val].visible).attr('id', problem_list[val].id);
						var td_visible = $('<td></td>').append(td_visible_button).appendTo(item_tr);


						var td_mod_button = $('<button class="btn btn-primary mod"></button>').text('修改').attr('id', problem_list[val].id);


						var td_mod = $('<td></td>').append(td_mod_button).appendTo(item_tr);
					}
					item_tr.appendTo(problem_item);
				}
			}
		});
	});
	
	
	problem_item.find('tr td button.mod').click(function () {
		var id = $(this).attr('id');
		problem_modify_init(id);
	});

	problem_item.find('tr td button.visible').click(function () {

		var id = $(this).attr('id');
		var button = $(this);
	
		up_data = {
			id: id,
		};
		$.ys_ajax({

			url: '/admin_oj/problem_visible/',
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
}

function problem_modify_init(id){
	KindEditor.remove('textarea[name=desc-modify]');
	editor_modify = init_editor('textarea[name=desc-modify]');
	
	$('#problem-list #problem-table').hide();
		$('#bt').hide();
		$('#problem-list #problem-modify').show();
		up_data = {
			id: id,
		};
		$.ys_ajax({
			url: '/admin_oj/problem_get/',
			data: up_data,
			type: 'GET',

			rt_func: function (data) {
				$('#id').html(data.problem.id);
				$('#title').html(data.problem.title);
				editor_modify.html(data.problem.description)
//				$('#desc').html(data.problem.description);
				$('#desc-input').html(data.problem.pro_input);
				$('#desc-output').html(data.problem.pro_output);
				$('#sample-input').html(data.problem.sample_input);
				$('#sample-output').html(data.problem.sample_output);
				$('#hint').html(data.problem.hint);
				$('#source').html(data.problem.source);
				$('#timelimit').html(data.problem.time_limit);
				$('#memorylimit').html(data.problem.memory_limit);
				$('#difficult').html(data.problem.difficult);
			}
		});
		init_problem_fix_page(id);
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

function problem_add() {

	var main_page = $('#problem-add').unbind();

	var flag = 0;
	var editor = init_editor('textarea[name=desc-content]');
	main_page.find('#submit-problem').click(function () {

		main_page.find('.form-control').each(function () {

			if ($(this).val() == '') {
				$(this).parent().addClass('has-error');

				$(this).focus(function () {
					$(this).parent().removeClass('has-error');
					$(this).unbind();
				});
				if ($(this).attr('id') != 'hint' && $(this).attr('id') != 'source')
					flag = 1;
			}
		});

		if (flag == 1)
			return;
		console.info(main_page.find('#title').val())

		up_data = {
			title: main_page.find('#title').val(),
			//			desc: main_page.find('#desc').val(),
			desc: editor.html(),
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

			url: '/admin_oj/problem_add/',
			data: up_data,
			type: 'POST',

			rt_func: function (data) {
				if (data.status == 200) {
					alert('添加成功');
				} else {
					return;
				}
			}

		});
	});
}

function init_problem_fix_page(p_id) {

	problem_fix();
}

function problem_fix() {
	var main_page = $('#problem-modify').unbind();
	var flag = 0;
	main_page.find('#fix-problem').click(function () {

		main_page.find('.form-control').each(function () {

			if ($(this).val() == '') {
				$(this).parent().addClass('has-error');

				$(this).focus(function () {
					$(this).parent().removeClass('has-error');
					$(this).unbind();
				});
				if ($(this).attr('id') != 'hint' && $(this).attr('id') != 'source')
					flag = 1;
			}
		});

		if (flag == 1)
			return;

		up_data = {
			id: main_page.find('#id').val(),
			title: main_page.find('#title').val(),
//			desc: main_page.find('#desc').val(),
			desc : editor_modify.html(),
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
			url: '/admin_oj/problem_fix/',
			data: up_data,
			type: 'POST',

			rt_func: function (data) {
				if (data.status == 200) {
					alert('修改成功!!');
				} else {
					alert('修改失败!!');
				}
			}

		});
	});

	main_page.find('#problem-modify-back').click(function () {
		$('#problem-list #problem-modify').hide();
		$('#problem-list #problem-table').show();
		$('#bt').show();
	});
}

function problem_rejudge() {
	var main_page = $('#problem-rejudge');
	main_page.find('#p-rejudge').unbind().click(function(){
		var id = main_page.find('#p_id').val();
		up_data = {
			id: id,
		}
		$.ys_ajax({
			url : '/admin_oj/problem_rejudge/',
			data : up_data,
			type : 'GET',
			
			rt_func: function(data){
				if(data.status == 200){
					alert('重判成功～');
				}
				else{
					alert('重判失败～');
				}
			}
		});
	});
	
	main_page.find('#s-rejudge').unbind().click(function(){
		var id = main_page.find('#s_id').val();
		up_data = {
			id: id,
		}
		$.ys_ajax({
			url : '/admin_oj/solution_rejudge/',
			data : up_data,
			type : 'GET',
			
			rt_func: function(data){
				if(data.status == 200){
					alert('重判成功～');
				}
				else{
					alert('重判失败～');
				}
			}
		});
	});
}