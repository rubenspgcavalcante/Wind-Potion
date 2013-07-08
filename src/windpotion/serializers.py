from datetime import datetime, date, timedelta
from tornado.escape import json_encode

__author__ = 'Rubens Pinheiro'
__date__ = '02/07/13 16:14'


class Serializer(object):
    def filter(self, value):
        if type(value) in (str, unicode, int, float, bool):
            return value

        elif isinstance(value, datetime) or isinstance(value, date):
            return value.isoformat()

        elif isinstance(value, timedelta):
            return (datetime.datetime.min + value).time().isoformat()

        elif type(value) is dict:
            for i in value:
                val = self.filter(value[i])
                value.update({i: val})

            return value

        elif type(value) is list:
            res = []
            for i in value:
                res.append(self.filter(i))

            return res

    def elixirToDict(self, obj, deep={}, excludes={}):
        dictObj = obj.to_dict(deep, excludes)
        for val in dictObj:
            dictObj[val] = self.filter(dictObj[val])

        return dictObj

    def entitiesToJSON(self, objects, deep={}, excludes={}):
        formatted = []
        for obj in objects:
            formatted.append(self.entityToJson(obj, deep, excludes))

        return json_encode(formatted)

    def entityToJson(self, object, deep={}, excludes={}):
        return self.elixirToDict(object, deep, excludes)