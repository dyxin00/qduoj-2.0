# encoding:utf-8   
from django import template
from django.template import resolve_variable

PAGE_NUM = 4
register = template.Library()   

class RankNode(template.Node):

    def __init__(self, page, msg):
        self.page = page
        self.msg = msg

    def render(self, context):
        try:
            page = template.resolve_variable(self.page, context) 
            msg = template.resolve_variable(self.msg, context) 
            return str((int(page) - 1) * PAGE_NUM + int(msg))
        except template.VariableDoesNotExist:
            return '0'

@register.tag
def rank_tag(parser,token):
    try:
        tag_name, page, msg = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]

    return RankNode(page, msg)

