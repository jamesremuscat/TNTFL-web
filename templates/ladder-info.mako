<%!
from datetime import datetime
%>

<p class="updated-time text-right">Updated at ${datetime.now().strftime("%d-%b-%Y %H:%M:%S")}</p>
<div class="controls form">
	<button class="btn btn-danger button_active form-control" onclick="$('.inactive').show(); $('.button_active').hide();">Show inactive</button>
	<button id="inactiveButton" class="form-control inactive" onclick="$('.inactive').hide(); $('.button_active').show();">Hide inactive</button>
</div>