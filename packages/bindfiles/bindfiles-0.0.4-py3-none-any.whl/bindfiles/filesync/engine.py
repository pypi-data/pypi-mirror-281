from __future__ import annotations
from typing import Optional, Callable, cast, Any, Type

import os
import json
#from flask import Request,  Flask, send_file, make_response,  jsonify #Response,


#other modules
from bindfiles.api.drive import Drive
from bindfiles.tools.funcs import flat
from bindfiles.api.drive import File
from bindfiles.tools.file_source import source, source_filter, source_par #File, 
from nbDevTools.nbCom.jupyter import IRequest, IResponse

#current - avoid cyclic
from bindfiles.filesync.schema import Ifile 
import bindfiles.filesync.schema as schema
import bindfiles.filesync.settings as settings

#def cria() -> None:
#    settings.LOAD_APP =  schema.config2

from flask import Request


class FileSource:
    def __init__(self, s : source_par) -> None:
        # self.e : schema.SOURCE_TYPE = schema.SOURCE_TYPE.NONE
        self.serv : source = source(s)
        # self._fapp = fApp        
        self.lt_file : list[schema.Ifile] = []

    # def gdrive(self,id:str , cred: str) -> None:
    #     self.e = schema.SOURCE_TYPE.PY_GDRIVE
    #     self.serv = source(folder= id, cred=cred, options=self._fapp.opt , stg_id= self._fapp._stg_id)

    # def local(self, path: str) -> None:
    #     self.e = schema.SOURCE_TYPE.PY_LOCAL
    #     self.serv = source(folder= path, options=self._fapp.opt )

    def listar(self) -> None:
        self.serv.listar(flat=False)

        self.lt_file = flat( cast(list[schema.Ifile], self.serv.lt_files) , add_folder=True, remove= True)
        for file in self.lt_file:
            file['isfile'] =  not 'childs' in file


class FileApp:
    _INST : str = '0x0'
    _DCI : dict[str,'FileApp'] = {}

    def __init__(self, a : source_par, b: source_par ) -> None:

        url_path : str = ''
        stg_id : str = ''
        
        self.INST = FileApp._INST[2:]
        FileApp._INST = hex(int(FileApp._INST,16) + 1)
        FileApp._DCI[self.INST] = self

        self.url_path = url_path #forma de acessar se tiver multiplos objetos mesmo flask
        self.pa = FileSource(a) #FileSource(self)
        self.pb = FileSource(b) #FileSource(self)
        self.stg : dict[str,Any]= {}
        self._stg_id : str = stg_id #id acessar oath gdrive
        
        self.lt : list[Any] = []

    def __delete__(self) -> None:
        FileApp._DCI.pop(self.INST)

    
    def resp_side(self, req : IRequest, fs: FileSource, Resp : Type[IResponse]) -> IResponse:
        #settings.LOG.write('resp side')
        

        qs = req.args #ImmutableMultiDict
        vs = (req.method, qs.get(settings.COMPILE_OPTIONS.FS_CMD.value, None))
        
        self.lt.append(f'vs= {vs}')
        # self.l t.append(fs)

        #settings.DEV['req'].append(vs)
        ARG_BLOB = settings.COMPILE_OPTIONS.FS_JSON_ARG_BLOB.value
        ARG_FILE = settings.COMPILE_OPTIONS.FS_JSON_ARG_FILE.value
        ARG_ID = settings.COMPILE_OPTIONS.FS_JSON_ARG_ID.value
        ARG_MOD = settings.COMPILE_OPTIONS.FS_JSON_ARG_MODIFIED.value
        ARG_INST = settings.COMPILE_OPTIONS.FS_QS_ARG_INST.value

        # if not req.trusted_hosts:
        #     return Resp(status=800)

        #settings.LOG.write(vs)
        # self.l t.append('try')
        try:
            #req.trusted_hosts.append('respside try')
            if ('GET', settings.COMPILE_OPTIONS.FS_CMD_LISTAR.value) == vs:
                fs.listar()
                
                return Resp(json.dumps(fs.lt_file), mimetype='application/json')
            
            elif ('POST', settings.COMPILE_OPTIONS.FS_CMD_GET.value) == vs: 
                body: Optional[dict[str, Any]] = req.get_json(silent=True) #AQUI BODY CONTEÚDO DO POST #Optional[dict[str, Any]]
                #settings.LOG.write(f'body={body} type body = {type(body)} req = {req}')
                if body:  #is not None and ARG_ID in body:            
                    fid : str = body[ARG_ID]            
                    content = fs.serv.get_blob(fid)
                    settings.LOG.write(f'conteúdo [{str(content)}]')
                    mimetype = "application/octet-stream"
                    return Resp(content, headers={"Content-Type": mimetype})

            elif ('POST', settings.COMPILE_OPTIONS.FS_CMD_CREATE.value) == vs: 
                file_create : File = json.loads(req.form[ARG_FILE])
                blob = req.files[ARG_BLOB].stream.read()
                nfile = fs.serv.create_file(name=file_create['name'],path=file_create['folder'], blob = blob, mimeType=file_create.get('mimeType',None))
                if 'modifiedTime' in file_create:
                    nfile = fs.serv.update_file(target=nfile,source={'modifiedTime':file_create['modifiedTime']})
                return Resp(json.dumps(nfile), mimetype='application/json')
            
            elif ('POST', settings.COMPILE_OPTIONS.FS_CMD_UPDATE.value) == vs:         
                file_update : File = json.loads(req.form[ARG_FILE])
                if ARG_BLOB in req.files:
                    blob = req.files[ARG_BLOB].stream.read()
                    file_update = fs.serv.write_blob(file_update,blob)            
                if ARG_MOD in req.form:
                    modtime : str = req.form[ARG_MOD]
                    file_update = fs.serv.update_file(file_update,{'modifiedTime':modtime })    
                return Resp(json.dumps(file_update), mimetype='application/json')           
                
            elif ('POST', settings.COMPILE_OPTIONS.FS_CMD_DEL_ITEM.value) == vs:         
                body = req.get_json(silent=True)
                file_delete : File = body[ARG_FILE] # type: ignore
                fs.serv.file_delete(file_delete['id'])  
                return Resp(status=204)           

            elif ('POST', settings.COMPILE_OPTIONS.FS_CMD_DEL_PATH.value) == vs:         
                body = req.get_json(silent=True)
                path : str = body[ARG_FILE] # type: ignore
                #settings.LOG.write('reg args path = ' + str(path))
                if path:
                    try:
                        fs.serv.path_delete(path)
                    except:
                        raise RuntimeError('Erro no path mesmo')
                    #settings.LOG.write(f'apagou path {path}')
                    return Resp(status=204)                                  
        except Exception as e:
            #lt_log.append(str(e))
            # settings.LOG.on_exception(e)
            raise e
            #req.trusted_hosts.append('respside try excep:' + str(e))     
            #settings.DEV['req'].append('excep:' + str(e))     

        
        raise NotImplementedError()

    def resp_stg(self, req : IRequest, Resp : type[IResponse] ) -> IResponse:
        ''' formar de armazenar em dict o que seria gravado em indexDB no JavasScript '''
        
        
        key = req.args.get(settings.COMPILE_OPTIONS.STORE_KEY.value, None) 
        #x = {'oi':key, 'dict': req.args.to_dict(), 'key': COPT.STORE_KEY.name}
        #return Response(json.dumps(x), mimetype='application/json')
        if req.method == 'GET':
            #rd.stg = {'width.0': 5, 'width.1':500, 'width.2': 2 }
            # self.l t.append(f'stg GET {key}')
            if key:                
                ret_value = None if key not in self.stg else self.stg[key]
                # self.l t.append(f'stg GET key={key} value = {ret_value}')
                return Resp(json.dumps(ret_value), mimetype='application/json')
        elif req.method == 'POST':
            # self.l t.append(f'stg POST {key}')
            if key:
                self.stg[key] = req.get_json(silent=True)
                # self.l t.append(f'stg POST {key} value = {self.stg[key]}')
                #return Response(json.dumps(rd.stg), mimetype='application/json')
                return Resp('', status=200 )
            #return Response('check', status=200 )
        elif req.method == 'DELETE':
            
            # self.l t.append(f'stg DELETE {key}')
            if key:
                self.stg.pop(key, None)
            else:
                self.stg.clear()

        return Resp(json.dumps(req.args), mimetype='application/json')        
        
        #return Response(json.dumps(fs.lt_file), mimetype='application/json')    






    # def resp_side0(self, req : Request, fs: FileSource ) -> IResponse:
    #     req.form
    #     req.files
    #     req.get_json()
    #     raise RuntimeError('dev')


    
    # @staticmethod
    # def route_module(req : Request) ->  Optional[Response]:         
    #     url_base = req.path.split('/')[-1]
        
    #     arg_path = req.args.get(settings.COMPILE_OPTIONS.FS_QS_ARG_INST.value, None) #None padrão, permitir aplicações rodando 
        
    #     qs = req.args #ImmutableMultiDict
    #     vs = (req.method, qs.get(settings.COMPILE_OPTIONS.FS_CMD.value, None))        
    #     return FileApp.interface(web=True, arg_path=arg_path, url_base=url_base, vs=vs, qs = qs)[0]

    # @staticmethod
    # def interface(*, web : bool, method : str, arg_path : str, url_base : str, vs: str, qs : dict[str,str])-> tuple[Optional[Response], Any]:
    #     rd : FileApp = settings.RUNNING_DATA[ arg_path  ]
    #     if url_base  == settings.COMPILE_OPTIONS.FS_PATH_LEFT.value:
    #         return rd.resp_side(req, rd.pa )
        
    #     elif url_base == settings.COMPILE_OPTIONS.FS_PATH_RIGHT.value:
    #         return rd.resp_side(req, rd.pb )
            
    #     elif url_base == settings.COMPILE_OPTIONS.PATH_STORE.value:
    #         return rd.resp_stg(req)
    



