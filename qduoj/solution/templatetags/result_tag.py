# encoding:utf-8   
from django import template
from django.template import resolve_variable

register = template.Library()   


class LangNode(template.Node):

    language = ['C', 'C++', '', 'Java'] + [''] * 2
    def __init__(self, solution, msg):
        self.solution = solution
        self.msg = msg

    def render(self, context):
        try:   
            result = template.resolve_variable(self.solution, context)   
            return LangNode.language[int(result)]   
        except template.VariableDoesNotExist:   
            return ''
@register.tag
def language_tag(parser,token):   
    try:   
        tag_name, solution ,msg = token.split_contents()  
    except ValueError:   
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]   

    return LangNode(solution, msg)


class ResultNode(template.Node):
    answer = ['Pending'] * 4 + ['Accepted', 'Presentation Error',
                                'Wrong Answer', 'Time Limit',
                                'Memory Limit', 'Output Limit',
                                'Runtime Error', 'Compile Error'
                                ]
    flag = ['default'] * 4 + ['success', 'warning', 'danger'] + ['warning'] * 5 + [''] * 2
    button = '<button type="button" class="btn btn-%s btn-block btn-xs"> %s </button>'
    def __init__(self, result, msg):
        self.result = result
        self.msg = msg
    def render(self, context):
        
        try:   
            result = template.resolve_variable(self.result, context)   
            return ResultNode.button % (ResultNode.flag[int(result)], ResultNode.answer[int(result)])
        except template.VariableDoesNotExist:   
            return ''

@register.tag
def result_tag(parser, token):

    try:   
        tag_name, result, msg = token.split_contents()  
    except ValueError:   
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]   

    return ResultNode(result, msg)
