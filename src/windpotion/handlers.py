from tornado.escape import json_decode, json_encode
from tornado.web import RequestHandler, HTTPError
from windpotion.errors import DatabaseException
from windpotion.serializers import Serializer
from windpotion import decorators

__author__ = 'Rubens Pinheiro'
__email__ = "rubenspgcavalcante@gmail.com"
__date__ = "07/07/13 20:08"

class RestHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(RestHandler, self).__init__(application, request, **kwargs)
        self.serializer = Serializer()
        self.set_header("Content-type", "application/json")

    def filterJsonContent(self):
        content_type = self.request.headers.get("Content-Type", "")

        if content_type.startswith("application/json"):
            return json_decode(self.request.body)

        return None

    def get(self, id, **kwargs):
        if id != "":
            id = json_decode(id)
            result = self._service.findById(id)
            if result is None:
                return json_encode(None)
            else:
                self.write(self.serializer.entityToJson(result))
        else:
            results = self._service.list()
            self.write(self.serializer.entitiesToJSON(results))

    def post(self, dict_args=None, **kwargs):
        params = self.filterJsonContent()
        if params is None:
            params = {k: ''.join(v) for k,v in self.request.arguments.iteritems()}

        try:
            self._service.create(params)
            self.write(json_encode({}))

        except DatabaseException as e:
            self.set_status(400)
            self.finish(json_encode({'error': True, 'message': e.message}))

    def put(self, dict_args=None, **kwargs):
        params = self.filterJsonContent()
        if params is None:
            params = {k: ''.join(v) for k,v in self.request.arguments.iteritems()}

        #If the call is from a child class, use the argument parameter dict_args
        if params is None:
            params = dict_args

        try:
            if not hasattr(params, 'id'):
                raise HTTPError(400)

            self._service.save(params)
            self.write(json_encode({}))

        except DatabaseException as e:
            self.set_status(400)
            self.finish(json_encode({'error': True, 'message': e.message}))

    def delete(self, id, **kwargs):
        if id != "":
            id = json_decode(id)

            try:
                self._service.delete(id)
                self.write(json_encode({}))

            except DatabaseException as e:
                self.set_status(400)
                self.finish(json_encode({'error': True, 'message': e.message}))

    @staticmethod
    def getRouter(handler):
        return [(r'/%s/?(?P<id>[0-9]*)' % handler.Service.Entity.__name__.lower(), handler)]

class SecureRestHandler(RestHandler):
    def __init__(self, application, request, **kwargs):
        super(SecureRestHandler, self).__init__(application, request, **kwargs)

    @decorators.authenticated
    def get(self, id, **kwargs):
        return super(SecureRestHandler, self).get(id, **kwargs)

    @decorators.authenticated
    def post(self, dict_args=None, **kwargs):
        return super(SecureRestHandler, self).post(dict_args=None, **kwargs)

    @decorators.authenticated
    def put(self, dict_args=None, **kwargs):
        return super(SecureRestHandler, self).post(dict_args=None, **kwargs)

    @decorators.authenticated
    def delete(self, id, **kwargs):
        return super(SecureRestHandler, self).delete(id, **kwargs)