<%page args="title, body, classes='', style=''"/>
<div class="col-sm-3">
  <div class="panel panel-default panel-statbox">
    <div class="panel-heading">
      <h3 class="statbox">${title}</h3>
    </div>
    <div class="panel-body ${classes}" style="${style}">
      ${body}
    </div>
  </div>
</div>