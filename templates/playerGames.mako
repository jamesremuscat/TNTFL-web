<%!
title = ""
base = "../../../"
%>
<%inherit file="html.mako" />
  ${self.blocks.render("gamesListPage", pageTitle=pageTitle, games=games, base=self.attr.base)}
