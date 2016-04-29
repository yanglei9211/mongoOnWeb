#!/usr/bin/env python
# encoding=utf-8
#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class testHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('test.html')