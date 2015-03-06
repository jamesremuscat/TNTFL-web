from mako.lookup import TemplateLookup
from mako import exceptions

tl = TemplateLookup(directories=['templates'])


def serve_template(templatename, **kwargs):
    print get_template(templatename, **kwargs)


def get_template(templatename, **kwargs):
    mytemplate = tl.get_template(templatename)
    try:
        return mytemplate.render(**kwargs)
    except:
        return exceptions.text_error_template().render()


def redirect_302(redirectionTo):
    print "Status: 302 Found"
    print "Location: " + redirectionTo
    print
