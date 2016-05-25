from datetime import date
from flask import abort, Flask, redirect, request, Response
from tntfl.ladder import Game, TableFootballLadder
from tntfl.web import get_template

import time
import tntfl.templateUtils as utils


app = Flask(__name__)


def getLadder(timeRange=None):
    return TableFootballLadder("ladder.txt", timeRange=timeRange)


def jsonny(jsonText):
    return Response(jsonText, content_type="application/json")


@app.route("/")
def index():
    return get_template("index.mako", ladder=getLadder())


@app.route("/stats/")
def stats():
    return get_template("stats.mako", ladder=getLadder())


@app.route("/game/add/", methods=['GET', 'POST'])
@app.route("/game/add/<respFormat>", methods=['GET', 'POST'])
def game_add(respFormat=None):
    ladder = getLadder()
    form = request.form
    if "bluePlayer" in form and "redPlayer" in form:
            redScore = form["redScore"] if "redScore" in form else 0
            blueScore = form["blueScore"] if "blueScore" in form else 0
            game = ladder.addAndWriteGame(form["redPlayer"], redScore, form["bluePlayer"], blueScore)
            if respFormat == "json":
                return jsonny(get_template("json/wrappedGame.mako", game=game, ladder=ladder))
            else:
                return redirect("/game/%.0f" % game.time)
    abort(400)


@app.route("/game/<int:gameTime>/")
@app.route("/game/<int:gameTime>/<respFormat>")
def game_show(gameTime, respFormat=None):
    ladder = getLadder()
    for game in ladder.games:
        if game.time == gameTime:
            if respFormat == 'json':
                return jsonny(get_template("json/wrappedGame.mako", game=game, ladder=ladder))
            return get_template("wrappedGame.mako", game=game, ladder=ladder)
    abort(404)


@app.route("/ladder.cgi")
def ladder_cgi():
    form = request.args
    if "gamesFrom" in form and "gamesTo" in form:
        timeRange = (int(form["gamesFrom"]), int(form["gamesTo"]))
    else:
        timeRange = None
    if "base" in form:
        base = form["base"]
    else:
        base = ""
    return ladder_ajax(
        form['sortCol'] if "sortCol" in form else None,
        form["sortOrder"] if "sortOrder" in form else None,
        form["showInactive"] if "showInactive" in form else 0,
        timeRange=timeRange,
        base=base
    )


def ladder_ajax(sortCol, sortOrder, showInactive, timeRange=None, base=""):
    return get_template("ladder.mako", ladder=getLadder(timeRange), base=base,
                        sortCol=sortCol,
                        sortOrder=sortOrder,
                        showInactive=showInactive
                        )


@app.route("/ladder/json")
def ladder_json():
    return jsonny(get_template("json/ladder.mako", ladder=getLadder()))


@app.route("/recent.cgi")
def recent_cgi():
    form = request.form
    return recent_ajax(form['limit'] if 'limit' in form else 10)


def recent_ajax(limit=10):
    ladder = getLadder()
    return get_template("recent.mako", ladder=ladder, games=ladder.games, base="", limit=limit)


@app.route("/recent/json")
def recent_json():
    ladder = getLadder()
    return jsonny(get_template("json/recent.mako", ladder=ladder, games=ladder.games, base="", limit=10))


@app.route("/historic.cgi")
@app.route("/historic/")
def historic():
    form = request.form
    if "gamesFrom" in form and "gamesTo" in form:
        fromTime = int(form["gamesFrom"])
        toTime = int(form["gamesTo"])
        timeRange = (fromTime, toTime)
    else:
        epoch = date.fromtimestamp(0)
        startdate = date.today().replace(day=1)
        enddate = startdate.replace(month=startdate.month + 1) if startdate.month < 12 else date(startdate.year + 1, 1, 1)
        start = (startdate - epoch).total_seconds()
        end = (enddate - epoch).total_seconds()
        timeRange = (start, end)
    return historic_range(timeRange)


def historic_range(timeRange):
    return get_template("historic.mako", base="../", timeRange=timeRange)


@app.route("/player/<playerName>/")
@app.route("/player/<playerName>/<respFormat>")
def player(playerName, respFormat=None):
    ladder = getLadder()
    if playerName.lower() in ladder.players:
        if respFormat == "json":
            return jsonny(get_template("json/player.mako", player=ladder.players[playerName.lower()], ladder=ladder))
        else:
            return get_template("player.mako", player=ladder.players[playerName.lower()], ladder=ladder)
    else:
        abort(404)


@app.route("/player/<playerName>/games/")
@app.route("/player/<playerName>/games/<respFormat>")
def player_games(playerName, respFormat=None):
    ladder = getLadder()
    if playerName.lower() in ladder.players:
        player = ladder.players[playerName.lower()]
        if respFormat == 'json':
            return jsonny(get_template("json/playerGames.mako", pageTitle="%s's games" % player.name, games=player.games, ladder=ladder))
        else:
            return get_template("playerGames.mako", pageTitle="%s's games" % player.name, games=player.games, ladder=ladder)
    else:
        abort(404)


@app.route("/achievements/")
def achievements():
    ladder = getLadder()

    return get_template("achievements.mako",
                        ladder=ladder,
                        achievements=sorted(ladder.getAchievements().iteritems(), reverse=True, key=lambda t: t[1]))


@app.route("/headtohead/<playerOne>/<playerTwo>/")
def head_to_head(playerOne, playerTwo):
    ladder = getLadder()
    if playerOne.lower() in ladder.players and playerTwo.lower() in ladder.players:
        return get_template("headtohead.mako",
                            ladder=getLadder(),
                            depth=2,
                            player1=ladder.players[playerOne],
                            player2=ladder.players[playerTwo]
                            )
    else:
        abort(404)


@app.route("/headtohead/<playerOne>/<playerTwo>/games")
def head_to_head_games(playerOne, playerTwo):
    ladder = getLadder()
    if playerOne.lower() in ladder.players and playerTwo.lower() in ladder.players:
        player1=ladder.players[playerOne]
        player2=ladder.players[playerTwo]
        games = utils.getSharedGames(player1, player2)
        return get_template(
            "headtoheadgames.mako",
            ladder=getLadder(),
            depth=2,
            player1=player1,
            player2=player2,
            games=games
        )
    else:
        abort(404)


@app.route("/speculate/", methods=['GET', 'POST'])
def speculate():
    form = request.form
    previousGames = ""

    if "previousGames" in form:
        previousGames = form["previousGames"]

    if "redPlayer" in form and "bluePlayer" in form:
        redScore = form["redScore"] if "redScore" in form else 0
        blueScore = form["blueScore"] if "blueScore" in form else 0
        previousGames += ",{0},{1},{2},{3}".format(form["redPlayer"], redScore, blueScore, form["bluePlayer"])

    if previousGames != "" and previousGames[0] == ",":
        previousGames = previousGames[1:]

    return speculate_with(previousGames)


def speculate_with(previousSpeculativeGames):
    gameParts = previousSpeculativeGames.split(",")
    ladder = getLadder()
    games = []

    for i in range(0, len(gameParts) / 4):
        g = Game(gameParts[4 * i], gameParts[4 * i + 1], gameParts[4 * i + 3], gameParts[4 * i + 2], time.time())
        games.append(g)
        ladder.addGame(g)

    games.reverse()

    return get_template("speculate.mako",
                        ladder=ladder,
                        games=games,
                        serialisedSpecGames=previousSpeculativeGames)


@app.route("/api/")
def api():
    return get_template("api.mako")

if __name__ == "__main__":
    app.run(debug=True)
