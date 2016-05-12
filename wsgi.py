from flask import abort, Flask, redirect, request
from tntfl.ladder import Game, TableFootballLadder
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


if __name__ == "__main__":
    app.run(debug=True)
