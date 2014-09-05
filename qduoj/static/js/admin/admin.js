cmd_map = {
    'problem-list' : init_problem_list,
	'problem-add'  : problem_add,
	'contest-list' : init_contest_list,
	'contest-add' : contest_add,
	'contest-sim' : contest_sim,
	'problem-rejudge' : problem_rejudge,
}
function init_menu(){
    $('#myTab').find('li').click(function(){
        var cmd = $(this).find('a').attr('cmd');
        cmd_map[cmd]();
    });
}
$(document).ready(function(){
    init_menu();
});
