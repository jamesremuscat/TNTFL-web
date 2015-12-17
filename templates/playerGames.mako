<%!
title = ""
base = "../../../"
%>
<%inherit file="html.mako" />
  ${self.blocks.render("gamesListPage", pageTitle=pageTitle, games=reversed(games), base=self.attr.base)}
