from marshmallow import Schema, fields
from flask import request
from urllib.parse import urlencode

class PaginationSchema(Schema):
    """ Schema which serialize the pagination object Flask-SQLAlchemy """
    class Meta:
        ordered = True

    links = fields.Method(serialize='get_pagination_links')
    page = fields.Integer(dump_only=True)
    pages = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)
    total = fields.Integer(dump_only=True)

    @staticmethod
    def get_url(page):
        """ Generate the URL of the page based on the page number """
        # Takes the pagenumber parameter and add it to the request argument's dict
        query_args = request.args.to_dict()
        query_args['page'] = page
        # encodes and returns the new URL, including the page number,as an argument
        return '{}?{}'.format(request.base_url, urlencode(query_args))

    def get_pagination_links(self, paginated_objects):
        """ Generates URL links to different pages. It gets the page's information
        from paginated_obkects and relies on the get_url() to generate links """
        pagination_links = {
            'first': self.get_url(page=1),
            'last': self.get_url(page=paginated_objects.pages)
        }

        if paginated_objects.has_prev:
            pagination_links['prev'] = self.get_url(page=paginated_objects.prev_num)

        if paginated_objects.has_next:
            pagination_links['next'] = self.get_url(page=paginated_objects.next_num)
        return pagination_links




