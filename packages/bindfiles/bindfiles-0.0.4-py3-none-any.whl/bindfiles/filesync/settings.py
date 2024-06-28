
from typing import Optional, Union, Any, TypedDict
import bindfiles.filesync.schema as schema
#from bindfiles.filesync.engine import FileApp
from enum import Enum
import os

import pkg_resources
#from pkg_resources import resource_stream
from websockets.legacy.server import WebSocketServerProtocol




#from gtools.tools.file_source import storage
#import filesync.capp as capp3


from enum import Enum

PACKAGE_NAME = __name__.split('.')[0]

class RESOURCE_FILES: #(str, Enum)
    FOLDER_HTML = 'html'
    FILE_OUTPUT_JS_COMPILED = 'html/__output__.js'
    FILE_HTML_FOR_JS = 'html/main.html'   
    FILE_DEBUG = 'html/debug.txt'
    #PATH_JS_COMPILED = pkg_resources.resource_filename(PACKAGE_NAME, os.path.join(RESOURCE_FILES.FOLDER_HTML,_FILE_OUTPUT_JS_COMPILED))


#LOAD_APP : Optional[schema.Config] = None

#RUNNING : dict[str,tuple[storage,storage]]= {}
# RUNNING_DATA : dict[ str, FileApp] = {}
RUNNING_FLASK_SERVER : set[str] = set()


# class WebSocketDict(TypedDict):
#     PORT : Optional[int]
#     CONNECTED : dict[str,set[WebSocketServerProtocol]]
# WBSOCKET : WebSocketDict = {'CONNECTED':{}, 'PORT':None }

# WEBSOCKET_PORT : Optional[int] = None
# WEBSOCKET_CONNECTED : set[WebSocketServerProtocol] = set()
# msgs : list[str] = []




#ENUMERAÇÃO PARA MANTER CONSISTÊNCIA COM JAVASCRIPT
class COMPILE_OPTIONS(Enum):
    PATH_STORE = 'STW' #WEB STORAGE
    STORE_KEY = 'KS'
    
    PATH_FS_LEFT = 'PPA'
    PATH_FS_RIGHT = 'PPB'
    FS_CMD = 'CMD'
    FS_CMD_LISTAR = 'LISTAR'
    FS_CMD_GET = 'GET'
    FS_CMD_CREATE = 'CREATE'
    FS_CMD_UPDATE = 'UPDATE'  #UPDATE BLOB E MODIFIED TIME
    FS_CMD_DEL_ITEM = 'DELETE'
    FS_CMD_DEL_PATH = 'DELPATH'
    #FS_JSON_ARG_PAIR = 'PAIR'
    FS_JSON_ARG_ID = 'ID' #ARQUIVO EXISTENTE
    FS_JSON_ARG_FILE = 'FILE' #PASSAR DEFINIÇÕES
    FS_JSON_ARG_MODIFIED = 'MODIFIED'
    FS_JSON_ARG_BLOB = 'BLOB'
    FS_QS_ARG_INST = 'INST'   
    
    PATH_MSG = 'PMC'
    MC_CMD_GET_PORT_WEBSOCKET = 'GSPORT'
    MC_CMD_FORCE_RELOAD = 'WMSGRELOAD' #ATUALIZAR INSTÂNCIAS
    #nome /** @define {string} */ const MG_FORCE_REFRESH_RELOAD = goog.define('MG_FORCE_REFRESH_RELOAD','W%RLOAD$!');



DEV_LT : list[Any] =  []


import inspect
import traceback
from typing import Type, Optional, cast,Callable
from types import TracebackType, FrameType
import pkg_resources
from datetime import datetime
from typing_extensions import Self

class LogDebug:
    def __enter__(self) -> 'LogDebug':
        return self

    def __exit__(self, exc_type : Optional[Type[BaseException]], exc_value : Optional[BaseException], tb : TracebackType) -> bool:
        
        stack = traceback.extract_tb(tb)
        last_call = stack[-1]
        
        if exc_type is not None:
            
            t = f"Erro ocorreu no arquivo {last_call.filename}, linha {last_call.lineno}, em {last_call.name}" + '\n' + \
                f"Exceção capturada: {exc_type.__name__}, Mensagem: {exc_value}"
            self.write(t, add_date= True)
            #if  len(stack) == -1:
            return False  # Não trata a exceção, permite a propagação
        else:
            return True #trata exceção mas aqui não tem nenhuma
    
    @staticmethod
    def exception_str(e : Exception) -> str:
        #self.write(f"Exceção capturada: {type(e)}, Mensagem: {e}")
        #return

        le : list[str] = []
        le.append(f"Exceção capturada: {type(e)}, Mensagem: {e}")
        def se( tb : TracebackType) -> None:
            frame : FrameType = tb.tb_frame
            lc : inspect.Traceback = inspect.getframeinfo(frame)
            t = f"Erro: arquivo {lc.filename.split(os.path.sep)[-1]}, linha {lc.lineno}, em {lc.function}"
            le.append(f'{"   "*len(le)} {t}')

        
        tb = cast(TracebackType, e.__traceback__) # Extrai o último chamado antes da exceção ser levantada
        se(tb)
        while tb.tb_next:
            tb = tb.tb_next
            se(tb)
        #last_frame = tb.tb_frame
        #last_call = inspect.getframeinfo(last_frame)
        
        #current_frame = inspect.currentframe()
        #last_call = inspect.getouterframes(current_frame, 0)[1] #0 dentro do enter, 1 __init__ da classe , 2 : with classe()

        
        # se : Callable[[inspect.Traceback],None] = lambda lc :  le.append()
        # t = f"Erro: arquivo {last_call.filename.split(os.path.sep)[-1]}, linha {last_call.lineno}, em {last_call.function}" + '\n' + \
        #     f"Exceção capturada: {type(e)}, Mensagem: {e}"
        return '\n'.join(le)
    
    def on_exception(self, e : Exception) -> None:
        t = LogDebug.exception_str(e)
        self.write(t)
        
        
    def write(self, txt : Any, add_date : bool = True) -> None: 
        debug_file = pkg_resources.resource_filename(PACKAGE_NAME, RESOURCE_FILES.FILE_DEBUG)
        with open(debug_file,'a') as file:
            if add_date:
                file.write(f'\n{datetime.now().isoformat()}')
            file.write('\n' + str(txt))
LOG : LogDebug = LogDebug()
                