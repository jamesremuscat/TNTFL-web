from collections import OrderedDict
from flask import abort, Flask, redirect, request
from tntfl.ladder import Game, TableFootballLadder
from tntfl.achievements import Achievement
from tntfl.web import get_template

import time


app = Flask(__name__)


def getLadder():
    return TableFootballLadder("ladder.txt")


@app.route("/")
def index():
    return get_template("index.mako", ladder=getLadder())


@app.route("/stats/")
def stats():
    return get_template("stats.mako", ladder=getLadder())


@app.route("/game/add/", methods=['GET', 'POST'])
def game_add():
    ladder = getLadder()
    form = request.form
    if "bluePlayer" in form and "redPlayer" in form:
            redScore = form["redScore"] if "redScore" in form else 0
            blueScore = form["blueScore"] if "blueScore" in form else 0
            game = Game(form["redPlayer"], redScore, form["bluePlayer"], blueScore, time.time())
            ladder.addAndWriteGame(game)
            if "view" in form and form["view"] == "json":
                return get_template("wrappedGame.mako", game=game)
            else:
                return redirect("/game/%.0f" % game.time)


@app.route("/game/<int:gameTime>/")
def game_show(gameTime):
    found = False
    for game in getLadder().games:
        if game.time == gameTime and not found:
            return get_template("wrappedGame.mako", game=game)
            found = True
    if not found:
        abort(404)


@app.route("/ladder.cgi")
def ladder_cgi():
    form = request.form
    return ladder_ajax(form['sortCol'] if "sortCol" in form else None,
                       form["sortOrder"] if "sortOrder" in form else None,
                       form["showInactive"] if "showInactive" in form else 0
                       )


def ladder_ajax(sortCol, sortOrder, showInactive):
    return get_template("ladder.mako", ladder=getLadder(), base="",
                        sortCol=sortCol,
                        sortOrder=sortOrder,
                        showInactive=showInactive
                        )


@app.route("/recent.cgi")
def recent_cgi():
    form = request.form
    return recent_ajax(form['limit'] if 'limit' in form else 10)


def recent_ajax(limit=10):
    return get_template("recent.mako", ladder=getLadder(), base="", limit=limit)


@app.route("/player/<playerName>/")
def player(playerName):
    ladder = getLadder()
    if playerName.lower() in ladder.players:
        return get_template("player.mako", player=ladder.players[playerName.lower()], ladder=ladder)
    else:
        abort(404)


@app.route("/player/<playerName>/games/")
def player_games(playerName):
    ladder = getLadder()
    if playerName.lower() in ladder.players:
        return get_template("playerGames.mako", player=ladder.players[playerName.lower()], ladder=ladder)
    else:
        abort(404)


@app.route("/achievements/")
def achievements():
    ladder = getLadder()
    achievements = {}

    for ach in Achievement.achievements:
        achievements[ach.__class__] = len(ach.players)

    return get_template("achievements.mako",
                        ladder=ladder,
                        achievements=OrderedDict(sorted(achievements.iteritems(), reverse=True, key=lambda t: t[1])))


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
