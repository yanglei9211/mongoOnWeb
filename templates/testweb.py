#!/usr/bin/env python
# encoding=utf-8
#!/usr/bin/env python

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado import template
from tornado.options import define, options
from jinja2 import Environment, FileSystemLoader,ChoiceLoader
from template import JinjaLoader
import jinja2 as ja

define("port", default=8888, help="run on the given port", type=int)

class ShireWeb(object):
	def get_settings(self, proj_template_path, proj_static_paths):
		self_dir_path = os.path.abspath(os.path.dirname(__file__))

		loader = ChoiceLoader([
			FileSystemLoader(proj_template_path),
			FileSystemLoader(os.path.join(self_dir_path, 'templates')),
		])

		return{
			'template_loader' : JinjaLoader(loader=loader, auto_escape=False)
		}

	def __init__(self, routes, template_path, proj_static_paths=[]):
		the_settings = self.get_settings(template_path, proj_static_paths)
		self.app = Application(routes, **the_settings)

	def run(self):
		server = HTTPServer(self.app, xheaders=True)
		server.listen(options.port)
		tornado.ioloop.IOLoop.current().start()


def main():
	routes = [
		('/','testHandler')
	]
	template_path = 'templates'
	server = ShireWeb(routes, template_path)
	server.run()


print ja.Template("""\
<html>
	Hello {{user}}
	{{dt}}
	{% for i in dt %}
		{{i}}
	{%endfor%}
</html>
""").render(user='abc',dt=[1,2,3,4,5])