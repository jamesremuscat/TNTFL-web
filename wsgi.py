from flask import Flask
from tntfl.ladder import TableFootballLadder
from tntfl.web import get_template


app = Flask(__name__)


def strip_header(page):
    return page.replace("Content-Type: text/html", "")


@app.route("/")
def index():
    ladder = TableFootballLadder("ladder.txt")
    return strip_header(get_template("index.mako", ladder=ladder))

if __name__ == "__main__":
    app.run()
