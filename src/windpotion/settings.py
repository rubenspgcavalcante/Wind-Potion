from windpotion.utils import singleton

__author__ = 'Rubens Pinheiro'
__date__ = '09/07/13 10:42'

@singleton
class Options(object):
    def __init__(self):
        options = {
            "custom_validation": None,
        }
        self._setup(options)

    def _setup(self, dict_attrs):
        for attr in dict_attrs:
            setattr(self, attr, dict_attrs[attr])