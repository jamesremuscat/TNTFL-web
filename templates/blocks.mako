<%def name="render(templateFile, **kwargs)">
<%
from mako.lookup import TemplateLookup
from mako import exceptions
tl = TemplateLookup(directories=['templates'])
mytemplate = tl.get_template(templateFile + ".mako")
%>
    ${mytemplate.render(ladder=ladder, **kwargs)}
</%def>