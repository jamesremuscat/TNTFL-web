<%namespace name="blocks" file="blocks.mako"/>${value}
% if toDate > 0:
<div class="date">
From ${blocks.render("gameLink", time=fromDate, base=base)}<br/>
to ${blocks.render("gameLink", time=toDate, base=base)}
</div>
% else:
-
% endif