import requests
import os


def publishToSlack(game):
    if "SLACK_WEBHOOK_URL" in os.environ:
        webhookURL = os.environ["SLACK_WEBHOOK_URL"]
        rootURL = os.environ["TNTFL_ROOT_URL"]
        title = "{redPlayer} {redScore}-{blueScore} {bluePlayer}".format(
            redPlayer=game.redPlayer,
            redScore=game.redScore,
            blueScore=game.blueScore,
            bluePlayer=game.bluePlayer
        )
        title_url = rootURL + "game/{}".format(game.time)

        fields = []

        if game.skillChangeToBlue < 0:
            fields.append({
                "title": "{}'s skill".format(game.redPlayer),
                "value": "{:+.3f}".format(game.skillChangeToBlue * -1),
                "short": True
            })
        elif game.skillChangeToBlue > 0:
            fields.append({
                "title": "{}'s skill".format(game.bluePlayer),
                "value": "{:+.3f}".format(game.skillChangeToBlue),
                "short": True
            })

        if game.bluePosChange != 0:
            fields.append({
                "title": "{}'s ranking".format(game.bluePlayer),
                "value": "{:d} ({:+d})".format(game.bluePosAfter, game.bluePosChange),
                "short": True
            })

        if game.redPosChange != 0:
            fields.append({
                "title": "{}'s ranking".format(game.redPlayer),
                "value": "{:d} ({:+d})".format(game.redPosAfter, game.redPosChange),
                "short": True
            })

        footer = "TNTFL v3.5.0"

        message = {
            "attachments": [
                {
                    "pretext": "Final score:",
                    "title": title,
                    "title_link": title_url,
                    "fields": fields,
                    "footer": footer,
                    "ts": game.time
                }
            ],
            "username": "refbot",
            "icon_emoji": ":soccer:"
        }
        requests.post(webhookURL, json=message)