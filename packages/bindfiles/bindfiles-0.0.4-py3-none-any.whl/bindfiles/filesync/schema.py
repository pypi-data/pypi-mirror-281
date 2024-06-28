from typing import TypedDict
from enum import Enum


#Python Inline Source Syntax Highlighting
#from typing import Annotated
#source_code = Annotated[str, 'source_code']
#TML = Annotated[source_code, 'html']


class SOURCE_TYPE(Enum):
    NONE  = 0
    JS_LOCAL = 1
    JS_GDRIVE = 2
    PY_LOCAL = 3
    PY_GDRIVE = 4


class Ifile(TypedDict): #, total = False
    name : str
    folder : str
    mimeType : str
    modifiedTime : str
    size : int
    isfile : bool
    #childs : list['Ifile']




#class DEF_KEYS(TypedDict, total = False):
#    
#    COMPILE_SELETION : int







'''
class Config(TypedDict, total = False):
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str

config: Config = {
    'DEBUG': True,
    'DATABASE_URL': 'sqlite:///meubanco.db',
    'SECRET_KEY': 'uma_chave_super_secreta',
}


config2: Config = {
    'DATABASE_URL': 'sqlite:///meubanco.db',
    'SECRET_KEY': 'uma_chave_super_secreta',
}
'''