from elixir import session
from sqlalchemy.exc import IntegrityError
from tornado.escape import json_decode, json_encode
from tornado.web import RequestHandler, HTTPError
from windpotion.serializers import Serializer
from windpotion import annotations

__author__ = 'Rubens Pinheiro'
__email__ = "rubenspgcavalcante@gmail.com"
__date__ = "07/07/13 20:08"

class RestHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(RestHandler, self).__init__(application, request, **kwargs)
        self.serializer = Serializer()
        self.set_header("Content-type", "application/json")

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
        if dict_args is not None:
            params = dict_args
        else:
            params = {k: ''.join(v) for k,v in self.request.arguments.iteritems()}

        try:
            self._service.create(params)
        except IntegrityError:
            session.rollback()
            raise HTTPError(400)

    def put(self, dict_args=None, **kwargs):
        if dict_args is not None:
            params = dict_args
        else:
            params = {k: ''.join(v) for k,v in self.request.arguments.iteritems()}

        try:
            if params.get("id") is None:
                raise HTTPError(400)

            self._service.save(params)
        except IntegrityError:
            session.rollback()
            raise HTTPError(400)

    def delete(self, id, **kwargs):
        if id != "":
            id = json_decode(id)
            self._service.delete(id)

    @staticmethod
    def getRouter(handler):
        return [(r'/%s/?(?P<id>\d?)' % handler.Service.Entity.__name__.lower(), handler)]

class SecureRestHandler(RestHandler):
    def __init__(self, application, request, **kwargs):
        super(SecureRestHandler, self).__init__(application, request, **kwargs)

    @annotations.authenticated
    def get(self, id, **kwargs):
        return super(SecureRestHandler, self).get(id, **kwargs)

    @annotations.authenticated
    def post(self, dict_args=None, **kwargs):
        return super(SecureRestHandler, self).post(dict_args=None, **kwargs)

    @annotations.authenticated
    def put(self, dict_args=None, **kwargs):
        return super(SecureRestHandler, self).post(dict_args=None, **kwargs)

    @annotations.authenticated
    def delete(self, id, **kwargs):
        return super(SecureRestHandler, self).delete(id, **kwargs)