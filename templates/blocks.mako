<%def name="render(templateFile, **kwargs)">
<%
from tntfl.web import get_template
%>
  ${get_template(templateFile + ".mako", ladder=ladder, **kwargs)}
</%def>