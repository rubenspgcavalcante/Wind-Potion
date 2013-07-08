import functools
from tornado.web import HTTPError
from elixir import session

__author__ = 'Rubens Pinheiro'
__email__ = "rubenspgcavalcante@gmail.com"
__date__ = "03/07/13 22:26"

def REST(Service):
    """
    REST Handler annotation
    Links the REST handler with the respective service using
    a Metaclass handler
    """
    class RestHandlerMeta(object):
        def __init__(self, cls):
            self.cls = cls
            self.Service = Service

        def __call__(self, application, request, **kwargs):
            obj = self.cls(application, request, **kwargs)
            super(self.cls, obj).__init__(application, request, **kwargs)
            setattr(obj, "_service", self.Service())
            return obj

    return RestHandlerMeta

def service(Entity):
    """
    Generic Service annotation
    Links the service objects to the respective entity, giving some default basic methods
    using a Metaclass service
    """

    class ServiceMeta(object):
        def __init__(self, cls):
            self.cls = cls
            self.Entity = Entity

        def __call__(self, *args, **kwargs):
            obj = self.cls(*args, **kwargs)
            obj._meta = self
            obj._entity = self.Entity

            availableMethods = ['list', 'findById', 'create', 'save', 'delete']

            for method in availableMethods:
                if(not hasattr(obj, method)):
                    setattr(obj, method, getattr(self, method))

            return obj

        def list(self, limit=None, orderBy=None):
            record = self.Entity.query
            if type(orderBy) is list:
                for order in orderBy:
                    record = record.order_by(order)

            elif orderBy is not None:
                record = record.order_by(orderBy)

            if limit:
                record = record.limit(limit)

            return record.all()

        def findById(self, id):
            return self.Entity.get_by(id=id)

        def create(self, dict_attrs):
            obj = self.Entity()
            obj.from_dict(dict_attrs)
            session.add(obj)
            session.commit()

        def save(self, dict_attrs):
            obj = self.Entity.get_by(id=dict_attrs["id"])
            obj.from_dict(dict_attrs)
            session.commit()

        def delete(self, id):
            obj = self.Entity.get_by(id=id)
            obj.delete()
            session.commit()

    return ServiceMeta

def authenticated(method):
    """
    A default REST authenticate annotation
    If user isn't logged (using as reference the handler current_user),
    raises a 403 HTTP error. Doesn't redirects.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403)

        return method(self, *args, **kwargs)
    return wrapper