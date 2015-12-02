<%page args="time, base"/>
<%!
import tntfl.templateUtils as utils
%>
<a href="${base}game/${time}/">
  ${utils.formatTime(time)}
</a>
