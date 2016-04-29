#!/usr/bin/env python
# fileencoding=utf-8

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import BytecodeCache
import json
import tornado.escape
from bson.objectid import ObjectId
import datetime

json_decode = tornado.escape.json_decode

type_encoders = [
    (ObjectId, str),
]

def json_encode(value, ensure_ascii=False, indent=None):
    # adapted from tornado.escape.json_encode
    return json.dumps(
        value, default=objectid_encoder,
        ensure_ascii=ensure_ascii,
        indent=indent).replace("</", "<\\/")

def objectid_encoder(obj):
    for encoder in type_encoders:
        if isinstance(obj, encoder[0]):
            return encoder[1](obj)
    raise TypeError("Unknown value '%s' of type %s" % (
        obj, type(obj)))



def guess_autoescape(template_name):
    if template_name is None or '.' not in template_name:
        return False
    ext = template_name.rsplit('.', 1)[1]
    return ext in ('html', 'htm', 'xml')


def _ts_format(ts, format=None):
    dt = datetime.datetime.fromtimestamp(ts)
    if format is None:
        return dt.strftime("%m-%d %H:%M")
    elif format == 'absolute':
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif format == 'onlydate':
        return dt.strftime('%m-%d')
    elif format == 'fulldate':
        return dt.strftime('%Y-%m-%d')
    else:
        return dt.strftime(format)

ts_format = _ts_format


def _num_to_word(num):
    assert isinstance(num, int)
    trans_dict = {
        '1': u'一',
        '2': u'二',
        '3': u'三',
        '4': u'四',
        '5': u'五',
        '6': u'六',
        '7': u'七',
        '8': u'八',
        '9': u'九',
        '0': u'零',
    }
    return u''.join([trans_dict[i] for i in str(num)])


class MemoryBytecodeCache(BytecodeCache):
    # TODO: consider to make a Redis based cache

    def __init__(self):
        self.cache = {}

    def load_bytecode(self, bucket):
        code = self.cache.get(bucket.key)
        if code:
            bucket.bytecode_from_string(code)

    def dump_bytecode(self, bucket):
        self.cache[bucket.key] = bucket.bytecode_to_string()

    def clear(self):
        self.cache = {}


class JinjaLoader(object):
    def __init__(self, **kwargs):
        super(JinjaLoader, self).__init__()
        auto_reload = kwargs.get('debug', True)
        loader = kwargs.get('loader')
        if not loader:
            root_path = kwargs.get('root_path')
            if not root_path:
                assert 'no loader could be selected!'
            loader = FileSystemLoader(root_path)
        auto_escape = kwargs.get('auto_escape', guess_autoescape)
        self.env = Environment(loader=loader,
                               autoescape=auto_escape,
                               extensions=['jinja2.ext.autoescape'],
                               trim_blocks=True,
                               lstrip_blocks=True,
                               cache_size=-1,  # no clean-up
                               bytecode_cache=MemoryBytecodeCache(),
                               auto_reload=auto_reload)

        additional_globals = {
            'ord': ord,
            'chr': chr,
            'unichr': unichr,
            'json_encode': json_encode,
        }
        self.env.globals.update(additional_globals)
        self.env.filters['ts_format'] = _ts_format
        self.env.filters['num_to_word'] = _num_to_word

    def load(self, name, parent_path=None):
        return JinjaTemplate(self.env.get_template(name))

    def reset(self):
        '''Reset the cache of compiled templates, required
           in debug mode.
        '''
        self.env.cache.clear()


class JinjaTemplate(object):
    def __init__(self, template):
        self.template = template

    def generate(self, **kwargs):
        # jinja uses unicode internally but tornado uses utf string
        return self.template.render(**kwargs).encode('utf-8')
