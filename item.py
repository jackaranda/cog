import datetime
from db import db

class Item(object):

	def __init__(self, owner=None, **kwargs):

		self.owner = owner
		self.data = {}
		
		fields = self.schema['fields']

		for key, value in kwargs.items():	
			
			if key in fields:	
				if 'type' in fields[key]:
					value = fields[key]['type'](value)
				else:
					value = repr(value)

				if 'filter' in fields[key]:
					value = fields[key]['filter'](value)

			self.data[key] = value

		for key, config in fields.items():

			if key not in self.data:
				if 'default' in config:
					self.data[key] = config['default']

		if 'created' not in self.data:
			self.data['created'] = datetime.datetime.now()
		if 'modified' not in self.data:
			self.data['modified'] = datetime.datetime.now()

	def __getattr__(self, key):
		if key in self.data:
			return self.data[key]
		else:
			raise AttributeError

	def __setattr__(self, key, value):

		fields = self.schema['fields']

		if key in fields:
				
			if 'type' in fields[key]:
				value = fields[key]['type'](value)
			else:
				value = repr(value)

			if 'filter' in fields[key]:
				value = fields[key]['filter'](value)

			newdata = self.data
			newdata[key] = value
			newdata['modified'] = datetime.datetime.now()
			super(Item, self).__setattr__('data', newdata)

		else:
			self.__dict__[key] = value


	def __repr__(self):

		return repr(self.data)

	def save(self):

		coll = db[self.schema['name']]
		coll.update(self.data)


	@classmethod
	def find(cls, **kwargs):

		coll = db[cls.schema['name']]
		items = coll.find(kwargs)

		return [cls(**item) for item in items]









