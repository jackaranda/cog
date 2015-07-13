from flask import Flask
from flask import request
from flask.views import MethodView
from page import Page

app = Flask(__name__)

class PageView(MethodView):

	def get(self, slug):
		page = Page.find(slug=slug)[0]
		page.content = "This is the content"
		page.save()
		return repr(page)

app.add_url_rule('/api/v1/page/<slug>/', view_func=PageView.as_view('page_api'))


if __name__ == '__main__':
    app.run()