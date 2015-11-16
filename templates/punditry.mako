<%page args="facts"/>
% if len(facts) > 0:
<div class="panel panel-default ">
  <div class="panel-heading">
    <h3 class="panel-title">Punditry</h3>
  </div>
  <div class="panel-body">
    % for fact in facts:
      ${fact.description}
    % endfor
  </div>
</div>
%endif
