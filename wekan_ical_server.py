import os
from wekanapi import WekanApi
from http.server import BaseHTTPRequestHandler, HTTPServer
import vobject
import dateutil.parser
import time

LISTEN_HOST = os.environ.get("LISTEN_HOST", default="127.0.0.1")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", default=8091))
WEKAN_HOST = os.environ["WEKAN_HOST"]
WEKAN_USER = os.environ["WEKAN_USER"]
WEKAN_PASSWORD = os.environ["WEKAN_PASSWORD"]
CACHE_SEC = int(os.environ.get("CACHE_SEC", default=-1))  # In seconds


def create_ical_event(cal, board, card, card_info):
    event = cal.add("vevent")
    event.add("summary").value = board.title + ": " + card_info["title"]
    event.add("dtstart").value = dateutil.parser.parse(card_info["dueAt"])
    if "description" in card_info:
        event.add("description").value = card_info["description"]
    event.add("url").value = WEKAN_HOST + "/b/" + board.id + "/x/" + card.id


class MyHandler(BaseHTTPRequestHandler):
    cachedResponse = b''
    lastUpdateTimestamp = 0

    def do_GET(s):
        curTimestamp = time.time()
        if curTimestamp - MyHandler.lastUpdateTimestamp > CACHE_SEC:
            MyHandler.lastUpdateTimestamp = curTimestamp

            wekan_api = WekanApi(
                WEKAN_HOST, {"username": WEKAN_USER, "password": WEKAN_PASSWORD}
            )

            cal = vobject.iCalendar()
            boards = wekan_api.get_user_boards()
            for board in boards:
                if board.title == 'Templates':
                    continue
                cardslists = board.get_cardslists()
                for cardslist in cardslists:
                    cards = cardslist.get_cards()
                    for card in cards:
                        info = card.get_card_info()
                        if "dueAt" in info and info["dueAt"] is not None:
                            create_ical_event(cal, board, card, info)

            MyHandler.cacheResponse = cal.serialize().encode()

        s.send_response(200)
        s.send_header("Content-type", "text/calendar")
        s.end_headers()
        s.wfile.write(MyHandler.cacheResponse)


if __name__ == "__main__":
    httpd = HTTPServer((LISTEN_HOST, LISTEN_PORT), MyHandler)
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()
