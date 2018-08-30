#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re
import requests
import simplejson as json
import socket
import time
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import urllib.request
import uuid

logging.basicConfig(
    format='%(asctime)s'
    ' | [%(filename)s:%(lineno)d] | %(levelname)s | %(message)s',
    level=logging.DEBUG)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [(r"/", HealthHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


class HealthHandler(tornado.web.RequestHandler):

    def get_value(self, text):
        text = text.replace(".", "")
        matchObj = re.search(r'r\$ *(\d{1,3}(\.\d{3})*|\d+)(\,\d{2})?', text)
        if matchObj:
            return float(
                matchObj.group().replace(
                    ",", ".").split(" ")[1])
        else:
            try:
                matchObj = int(re.findall(r'\d+', text)[0])
            except Exception as e:
                matchObj = 0
            if matchObj > 0:
                return matchObj
        return 0

    def get(self):
        self.write(":)")

    def post(self):
        data = json.loads(self.request.body)

        url = data.get("url")

        logging.info("Parsing URL: {}".format(url))

        name = int(time.time())
        urllib.request.urlretrieve(url, "/app/{}.ogg".format(name))

        os.system("opusdec /app/{name}.ogg /app/{name}.wav".format(name=name))
        os.system("sox /app/{name}.wav /app/{name}.flac".format(name=name))

        file = open("/app/{}.flac".format(name), "rb")

        try:
            response = requests.post(
                url="https://www.googleapis.com/upload/storage/v1/b/{}"
                "/o".format(os.environ["GS_STORAGE"]),
                params={
                    "uploadType": "media",
                    "name": "{}.flac".format(name),
                    "key": os.environ["GS_KEY"],
                },
                headers={
                    "Content-Type": "audio/flac",
                },
                data=file
            )
            logging.info("flac upload {}".format(response.content))
        except Exception as e:
            logging.error(e)
            self.write(json.dumps({
                "error": "GS_ERROR",
                "error_description": str(e)
            }))

        try:
            response = requests.post(
                url="https://speech.googleapis.com/v1/speech:recognize",
                params={
                    "key": os.environ["GS_KEY"],
                },
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps({
                    "audio": {
                        "uri": "gs://{}/{}.flac".format(
                            os.environ["GS_STORAGE"], name)
                    },
                    "config": {
                        "languageCode": "pt-BR"
                    }
                })
            )
            logging.info("speech text {}".format(response.content))
        except Exception as e:
            logging.error(e)
            self.write(json.dumps({
                "error": "SPEECH_ERROR",
                "error_description": str(e)
            }))

        os.remove("/app/{}.flac".format(name))
        os.remove("/app/{}.wav".format(name))
        os.remove("/app/{}.ogg".format(name))

        try:

            nlp_text = response.json().get(
                "results")[0].get("alternatives")[0]

            logging.info(nlp_text)

            response = requests.post(
                url="https://msging.net/commands",
                headers={
                    "Authorization": "Key {}".format(os.environ["BLIP_KEY"]),
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps({
                    "id": str(uuid.uuid1()),
                    "to": "postmaster@ai.msging.net",
                    "method": "set",
                    "type": "application/vnd.iris.ai.analysis-request+json",
                    "uri": "/analysis",
                    "resource": {
                        "text": nlp_text.get("transcript")
                    }
                })
            )
            logging.info("blip {}".format(response.content))

            entities = response.json().get("resource").get("entities")

            logging.info("entities {} | {}".format(entities, len(entities)))

            if len(entities) == 0:
                entities = {
                    "id": "categoria_gasto",
                    "name": "Categoria Gasto",
                    "value": "outros"
                }
            else:
                entities = entities[0]

            main_response = {
                "from_url": url,
                "to_url": "gs://{}/{}.flac".format(
                    os.environ["GS_STORAGE"], name),
                "speech": nlp_text,
                "value": self.get_value(nlp_text.get("transcript")),
                "nlp": {
                    "intention":
                        response.json().get("resource").get("intentions")[0],
                    "entities": entities
                }}

            logging.info("main response {}".format(main_response))

            self.write(json.dumps(main_response))
        except Exception as e:
            logging.error(e)
            self.write(json.dumps({
                "error": "SPEECH_ERROR",
                "error_description": str(e)
            }))


def main():
    app = Application()
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
