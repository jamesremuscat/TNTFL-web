<%page args="ladder, base, games, speculative=False"/>
<%namespace name="blocks" file="blocks.mako" />
<%!
from tntfl.pundit import Pundit
import tntfl.templateUtils as utils
%>
<%
  pundit = Pundit()
%>
% for game in games:
    ${blocks.render("game", game=game, base=base, punditryAvailable=utils.punditryAvailable(pundit, game, ladder), speculative=speculative)}
% endfor
