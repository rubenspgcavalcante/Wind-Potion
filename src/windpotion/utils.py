__author__ = 'Rubens Pinheiro'
__email__ = "rubenspgcavalcante@gmail.com"
__date__ = '09/07/13 11:52'

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance