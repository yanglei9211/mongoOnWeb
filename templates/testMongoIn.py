# encoding: utf-8
from pymongo import MongoClient
from bson.objectid import ObjectId

raw_q_ids = [
	ObjectId("57124864def2970a166522ab"),
	ObjectId("5712490cdef2970a166522b3"),
	ObjectId("57124966def2970a166522bb"),
	ObjectId("571249b4def2970a155f01fb"),
	ObjectId("57124a02def2970a155f0217"),
	ObjectId("57124bcbdef2970a155f023b"),
	ObjectId("57124c5cdef2970a155f0247"),
	ObjectId("57124ca2def2970a166522d1"),
	ObjectId("57124d00def2970a166522de"),
	ObjectId("57124d5adef2970a166522ea"),
	ObjectId("57124db4def2970a155f0257"),
	ObjectId("57124e39def2970a166522ff"),
	ObjectId("57124e96def2970a155f0267"),
	ObjectId("57124f75def2970a16652315"),
	ObjectId("5712520fdef2970a1665234d"),
	ObjectId("571252badef2970a1665235d"),
	ObjectId("571253d8def2970a16652375"),
	ObjectId("57125451def2970a155f02d8"),
	ObjectId("57125503def2970a166523a1"),
	ObjectId("571255dbdef2970a155f02e8"),
	ObjectId("571256c2def2970a155f0301"),
	ObjectId("571257efdef2970a155f0319"),
	ObjectId("5712eef2def2970a155f0444"),
	ObjectId("5712f0b6def2970a16652501"),
	ObjectId("5712f426def2970a155f0460")
]
parsed_q_ids = [
	ObjectId('57124864def2970a166522ac'),
	ObjectId('5712490cdef2970a166522b4'),
	ObjectId('57124966def2970a166522bc'),
	ObjectId('571249b4def2970a155f01fc'),
	ObjectId('57124a02def2970a155f0218'),
	ObjectId('57124bcbdef2970a155f023c'),
	ObjectId('57124c5cdef2970a155f0248'),
	ObjectId('57124ca2def2970a166522d2'),
	ObjectId('57124d00def2970a166522df'),
	ObjectId('57124d5adef2970a166522eb'),
	ObjectId('57124db4def2970a155f0258'),
	ObjectId('57124e39def2970a16652300'),
	ObjectId('57124e96def2970a155f0268'),
	ObjectId('57124f75def2970a16652316'),
	ObjectId('5712520fdef2970a1665234e'),
	ObjectId('571252badef2970a1665235e'),
	ObjectId('571253d8def2970a16652376'),
	ObjectId('57125451def2970a155f02d9'),
	ObjectId('57125503def2970a166523a2'),
	ObjectId('571255dbdef2970a155f02e9'),
	ObjectId('571256c2def2970a155f0302'),
	ObjectId('571257efdef2970a155f031a'),
	ObjectId('5712eef2def2970a155f0445'),
	ObjectId('5712f0b6def2970a16652502'),
	ObjectId('5712f426def2970a155f0461')
]
client = MongoClient('db-master.ecs.kuailexue.com', 28000)
db = client['math']
'''
res = db.parsed_q.find({'raw_q_id': {'$in': raw_q_ids}})
for i in res:
	print 'ObjectId(\'' + str(i['_id']) + '\')'
'''
res = db.item.find({'parsed_q_id': {'$in': parsed_q_ids}})
for i in res:
	id = i['parsed_q_id']

	par = db.parsed_q.find_one({'_id': id})
	raw = db.raw_q.find_one({'_id': par['raw_q_id']})
	print raw['volume_id']

	print i['q_tags']['edus'][0], i['q_tags']['edu_rep']
	print type(i['q_tags']['edus'][0]), type(i['q_tags']['edu_rep'])

	'''
	i['q_tags']['edus'][0] = 3
	i['q_tags']['edu_rep'] = 3
	db.item.save(i)
	'''
