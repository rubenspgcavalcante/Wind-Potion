__author__ = 'Rubens Pinheiro'
__email__ = "rubenspgcavalcante@gmail.com"
__date__ = "13/07/13 23:50"

class DatabaseException(Exception):
    def __init__(self, originalException, Entity):
        self.originalException = originalException
        self.Entity = Entity
        super(DatabaseException, self).__init__(originalException.message)