<%page args="title, body, classes='', style='', offset=0, width=3, caption=''"/>
<div class="col-sm-${width} col-md-offset-${offset * width}">
  <div class="panel panel-default panel-statbox" title="${caption}">
    <div class="panel-heading">
      <h3 class="statbox">${title}</h3>
    </div>
    <div class="panel-body ${classes}" style="${style}">
      ${body}
    </div>
  </div>
</div>