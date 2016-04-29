import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from template import JinjaLoader
from jinja2 import ChoiceLoader, FileSystemLoader
from tornado.options import define, options
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from collections import OrderedDict
from common import change_id_form
from common import recover_id_form
from common import show_pretty_dict
import json
subjects = ['math', 'physics', 'chemistry', 'biology', 'shire']

define("port", default=8004, help="run on the given port", type=int)


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html', data=[1, 2, 3, 4, 5, '1', 'a', 'c'])


class searchItemHandler(tornado.web.RequestHandler):
    def sorted(self, data):
        if isinstance(data, dict):
            if len(data) > 0 and (isinstance(data.keys()[0], int) or data.keys()[0].isdigit()):
                ans = OrderedDict(sorted(data.items(), key=lambda x: int(x[0])))
            else:
                ans = OrderedDict(sorted(data.items()))
                keys = ['stem', 'question', 'questions', 'options', 'answers']
                keydict = {v: k for k, v in enumerate(keys)}
                ans = OrderedDict(
                    sorted(ans.items(), key=lambda t: keydict[t[0]] if t[0] in keydict else 200))

            for key in ans:
                ans[key] = self.sorted(ans[key])
        elif isinstance(data, list):
            ans = []
            for d in data:
                ans.append(self.sorted(d))
        else:
            ans = data
        return ans

    def dumps(self, obj):
        obj = self.sorted(obj)
        return dumps(obj, ensure_ascii=False, indent=4, sort_keys=True)

    def get_item(self, item_id):
        return self.application.db.item.find_one({'_id':ObjectId(item_id)})

    def get_db(self,subject):
        return self.application.db_pool[subject]

    def get(self):
        db_names = self.application.db_names

        self.render('search.html')

    def post(self):
        action = self.get_argument('action')
        if action == 'search':
            ok = True
            try:
                id = self.get_argument('data')
                print id
                item = self.get_item(id)
                change_id_form(item)
                item = self.dumps(item)
            except Exception, e:
                ok = False
                item = e.message
            self.write({'ok': ok, 'data': item})

        else:
            pass


class showItemHandler(tornado.web.RequestHandler):
    def sorted(self, data):
        if isinstance(data, dict):
            if len(data) > 0 and (isinstance(data.keys()[0], int) or data.keys()[0].isdigit()):
                ans = OrderedDict(sorted(data.items(), key=lambda x: int(x[0])))
            else:
                ans = OrderedDict(sorted(data.items()))
                keys = ['stem', 'question', 'questions', 'options', 'answers']
                keydict = {v: k for k, v in enumerate(keys)}
                ans = OrderedDict(
                    sorted(ans.items(), key=lambda t: keydict[t[0]] if t[0] in keydict else 200))

            for key in ans:
                ans[key] = self.sorted(ans[key])
        elif isinstance(data, list):
            ans = []
            for d in data:
                ans.append(self.sorted(d))
        else:
            ans = data
        return ans

    def dumps(self, obj):
        obj = self.sorted(obj)
        return dumps(obj, ensure_ascii=False, indent=4, sort_keys=True)

    def get(self, item_id):
        ok = True
        try:
            item = self.get_item(item_id)
            item_dp = item
            change_id_form(item_dp)
            res = self.dumps(item_dp)
        except Exception, e:
            ok = False
            res = e.message
        self.render('test.html', ok=ok, data=res)

    def get_item(self, item_id):
        return self.application.db.item.find_one({'_id':ObjectId(item_id)})

if __name__ == "__main__":
    tornado.options.parse_command_line()
    loader = ChoiceLoader([
        FileSystemLoader('templates')
    ])
    client = MongoClient('10.0.0.168', 27017)
    db_pool = {}
    db_names = client.database_names()
    for s in db_names:
        db_pool[s] = client[s]
    app = tornado.web.Application({(r"/login", LoginHandler),
                                   (r"/item/?(\w*)", showItemHandler),
                                   (r"/search", searchItemHandler)
                                   },
                                  template_loader=JinjaLoader(loader=loader, auto_escape=True),
                                  static_path=os.path.join(os.path.dirname(__file__), "static"),
                                  debug=True
                                  )
    app.db_pool = db_pool
    app.db_names = db_names
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
