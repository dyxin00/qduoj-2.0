cmd_map = {
    'problem-list' : init_problem_list,
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
