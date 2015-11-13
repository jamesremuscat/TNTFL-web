<%namespace name="blocks" file="blocks.mako"/>${"{:.3f}".format(skill)}
<%page args="base, time"/>
<div class="date">
% if time > 0:
at ${blocks.render("gameLink", time=time, base=base)}
% else:
before first game
% endif
</div>