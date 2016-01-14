<%!
title = "API | "
base = "../"
%>
<%inherit file="html.mako" />
<div class="container-fluid">
  <div class="row">
    <div class="col-md-8">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h1 class="panel-title">Table Football API</h1>
        </div>
        <div class="panel-body">
          <p>A JSON API is available for ladder data.</p>
          <p>In the JSON returned, links to other resources are represented by an object with an 'href' property. The value of this property is the URI of the linked resource.</p>
          <ul>
            <li>
              <b>Player:</b> player/<i>&lt;playername&gt;</i>/json
              <ul>
                <li>Example: <a href="${self.attr.base}player/jrem/json">${self.attr.base}player/jrem/json</a></li>
              </ul>
            </li>
            <li>
              <b>Player games:</b> player/<i>&lt;playername&gt;</i>/games/json
              <ul>
                <li>Example: <a href="${self.attr.base}player/jrem/games/json">${self.attr.base}player/jrem/games/json</a></li>
                <li>Contains full game data, rather than href links; because of this, responses could be quite large.</li>
              </ul>
            </li>
            <li>
              <b>Game:</b> game/<i>&lt;gameid&gt;</i>/json
              <ul>
                <li>Example: <a href="${self.attr.base}game/1223308996/json">${self.attr.base}game/1223308996/json</a></li>
              </ul>
            </li>
            <li>
                <b>Games:</b> /games.cgi?view=json&from=<i>&lt;time&gt;</i>&to=<i>&lt;time&gt;</i>&includeDeleted=<i>&lt;0 or 1&gt;</i>
                <ul>
                    <li>Example: <a href="${self.attr.base}games.cgi?view=json&from=1443623743&to=1448897743">${self.attr.base}games.cgi?view=json&from=1443623743&to=1448897743</a>
                </ul>
            </li>
            <li>
              <b>Add Game:</b> game/add[/json] (POST)
              <ul>
                <li>Request should be a POST containing the following fields:
                  <ul>
                    <li>redPlayer</li>
                    <li>redScore</li>
                    <li>bluePlayer</li>
                    <li>blueScore</li>
                  </ul>
                </li>
                <li>If /json is appended to the URL, then the call will return a game resource representing the added game. Otherwise, the response will be a 302 redirect to the home page.</li>
              </ul>
            </li>
            <li>
              <b>Ladder:</b> <a href="${self.attr.base}ladder/json">ladder/json</a>
              <ul>
                <li>Some denormalised data is provided, to save having to fully resolve player hrefs.</li>
              </ul>
            </li>
            <li>
              <b>Recent games:</b> <a href="${self.attr.base}/recent/json">/recent/json</a>
              <ul>
                <li>Gives the ten most recent games in full.</li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
