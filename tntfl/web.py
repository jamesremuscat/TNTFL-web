from mako.lookup import TemplateLookup
from mako import exceptions
from tntfl.ladder import TableFootballLadder

tl = TemplateLookup(directories=['templates'])

t = TableFootballLadder("ladder.txt")


def serve_template(templatename, **kwargs):
    mytemplate = tl.get_template(templatename)
    try:
        print(mytemplate.render(ladder=t, **kwargs))
    except:
        print(exceptions.text_error_template().render())


def redirect_302(redirectionTo):
    print "302 " + redirectionTo
    print
