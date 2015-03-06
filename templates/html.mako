<%namespace name="blocks" file="blocks.mako" inheritable="True"/>Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${self.attr.title}</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/ladder.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <script src="js/jquery.min.js"></script>
    <script type="text/javascript" src="js/jquery.tablesorter.min.js"></script> 
    <script type="text/javascript" src="js/jquery.flot.min.js"></script> 
  </head>
  <body>
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <h3 class="navbar-text">Table Football Ladder</h3>
        </div>
    
        <form class="navbar-form navbar-right game-entry" method="post" action="game/add">
          <div class="form-group">
            <input type="text" name="redPlayer" class="form-control red player" placeholder="Red">
            <input type="text" name="redScore" class="form-control red score" placeholder="0" maxlength="2"> - <input type="text" name="blueScore" class="form-control blue score" placeholder="0" maxlength="2">
            <input type="text" name="bluePlayer" class="form-control blue player" placeholder="Blue">
            <script type="text/javascript">
              $(".red.score").change(function() {
                $(".blue.score").val(10 - $(".red.score").val());
              })
            </script>
          </div>
          <button type="submit" class="btn btn-default">Add game <span class="glyphicon glyphicon-triangle-right"></span></button>
        </form>
      </div><!-- /.container-fluid -->
    </nav>
    ${self.body()}
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>

</html>