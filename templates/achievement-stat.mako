<%page args="ach, count"/>
<div class="col-sm-3">
  <div class="panel panel-default panel-statbox panel-achievement" title="${ach.description}">
    <div class="panel-heading">
      <h3 class="statbox">${ach.name}</h3>
    </div>
    <div class="panel-body achievement-${ach.__name__}"">
      ${count}
    </div>
  </div>
</div>