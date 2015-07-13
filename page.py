from item import Item

def slug(string):
	return string.lower().replace(' ', '_')

class Page(Item):

	schema = {
		'name': 'Page',
		'fields': {
			'title': { 'type': str, 'filter': str.title },
			'content': { 'type': str },
			'slug': { 'type': str, 'filter': slug }
		}
	}



