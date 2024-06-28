
from typing import Optional, Any, cast, Callable, Type, Union, Mapping
import os
from datetime import datetime

#import importlib.resources as pkg_resources
import pkg_resources

import json
from flask import Request, Response, Flask, send_file, make_response,  jsonify
from ipykernel.comm import Comm #, CommManager

import ipywidgets as widgets
from IPython.display import display
from IPython.core.display import HTML




import anywidget #type : ignore
import traitlets

#from filesync.settings import PROJ_NAME, REPOSITORIES_DIR, REL_PATH_JS_DEV, REL_PATH_CLOSURE_PROJ_DEF, REL_PATH_CLOSURE_PROJ_OUT, REL_PATH_JS_PROJ
import re

#other
from nbDevTools.pyClosure import   path as _path
from nbDevTools import nbFlask as nbFlask
from nbDevTools.nbFlask import FServer
from nbDevTools.nbCom.jupyter import JN_MSG, IRequest, IResponse, NB_Reponse, NB_REQ, NB_Request #JN_Request, #2024-06-11

from IPython.display import  display
import secrets

#current
from bindfiles.tools.file_source import source, source_filter, source_par
import bindfiles.filesync.schema as schema
from bindfiles.filesync.engine import FileApp
import bindfiles.filesync.settings as settings

from typing import Protocol

import asyncio
import websockets
import threading

from typing import Set
from websockets.legacy.server import WebSocketServerProtocol

lws : list[Any] = []
async def route_ws(websocket : WebSocketServerProtocol, path : str) -> None:  #let ws = new WebSocket('ws://127.0.0.1:8765/beterraba'); #path = '/beterraba'
    
    inst = path[1:]
    #lista de websockets por path [=instância]
    sws = FileWidget._WS.get(inst,set()); sws.add(websocket)
    FileWidget._WS[inst] = sws

    try:
        async for message in websocket: # if conn == websocket:  # Evitar enviar a mensagem de volta ao remetente #     await conn.send('recebi ' + str(message))
            lws.append(message)
            lws.append(websocket)
            lws.append(path)

            fa = cast(Optional[FileWidget], FileApp._DCI.get(inst)) #path é usado para identificar as instâncias /0 , /1 .. 
            if fa:
                fa._msg_from_socket(websocket,message)
            
    finally:
        FileWidget._WS[inst].remove( websocket )


def route_module(req : IRequest, Resp : type[IResponse], lt_debug: list[Any] = []) ->  Optional[IResponse]:         
    #K = req.path[1:] == settings.COMPILE_OPTIONS.PATH_STORE.value
    #return Response(req.path + str(K), mimetype='text/plain')
    #req.trusted_hosts.append('rm try-2 ')

    lt_debug = settings.DEV_LT
    lt_debug.append(req.full_path)
    #lt_debug.append(f'route_path: {req.full_path}')
    
    try:
        rsplit = req.path.split('/')
        
        path = rsplit[-1]
        qs_inst = req.args.get(settings.COMPILE_OPTIONS.FS_QS_ARG_INST.value, '')        
        
        rd = FileApp._DCI.get(qs_inst)       
        if not rd and  len(rsplit) > 1:
            qs_inst = rsplit[-2]
            rd = FileApp._DCI.get(qs_inst)       

        if not rd:        
            lt_debug.append(f'sem FileApp em path {req.full_path}: qs {qs_inst}')

        else:
            lt_debug = rd.lt

            if path == settings.COMPILE_OPTIONS.PATH_FS_LEFT.value:
                lt_debug.append('route module: left')
                lt_debug.append((req, rd))
                lt_debug.append((req, rd.pa, Resp, lt_debug ))
                return rd.resp_side(req, rd.pa, Resp )
            
            elif path == settings.COMPILE_OPTIONS.PATH_FS_RIGHT.value:
                lt_debug.append('route module: right')
                return rd.resp_side(req, rd.pb, Resp)
                
            elif path == settings.COMPILE_OPTIONS.PATH_STORE.value:
                lt_debug.append('route module: stg')
                return rd.resp_stg(req, Resp )
            
            elif path == settings.COMPILE_OPTIONS.PATH_MSG.value:
                lt_debug.append('route module: msg')

                sender = req.args.get(settings.COMPILE_OPTIONS.MC_CMD_FORCE_RELOAD.value, None )
                if sender:
                    lt_debug.append(f'propagar {sender}') #... #propaga msg
                    return Response('combinado', mimetype='text/plain')

                if settings.COMPILE_OPTIONS.MC_CMD_GET_PORT_WEBSOCKET.value in req.args:
                    if FileWidget._WS_PORT:
                        return Response(f'ws://127.0.0.1:{FileWidget._WS_PORT}/{qs_inst}', mimetype='text/plain')
                    else:
                        return Response('NO WEBSOCKET', mimetype='text/plain')

                lt_debug.append(req.args.to_dict())
                return Response('no msg', mimetype='text/plain')

            else:
                lt_debug.append(f'NONE, route_path: {req.full_path}')
                pass
        
            
    except Exception as e:
        settings.LOG.on_exception(e)
        lt_debug.append(f'{type(e).__name__} {e}')        
        # req.trusted_hosts.append('erro' + str(e))
        return  Resp(f'{type(e).__name__} {e}', mimetype='text/plain')
    
    return None


def route_module_flask(req : Request) ->  Optional[Response]:   
    
    lt = settings.DEV_LT
    lt.append(('FLASK FULLPATH=',req.full_path))

    if req.full_path.startswith('/src/models/FoldersExplorer'):
        lt = settings.DEV_LT
        lt.append(('FLASK FULLPATH=',req.full_path))

    try:
        resp = route_module(req,Response, lt )     
        if isinstance(resp, Response): #só para adequar ao mypy
                return resp
    except Exception as e:
        lt.append(e)   

    return None
   


class FileWidget(FileApp):

    _WS_PORT : Optional[int] = None
    _WS : dict[str,set[WebSocketServerProtocol]] = {}
    _FS : Optional[FServer] = None
    _IP_HOST : str =  "127.0.0.1"

    def __init__(self, a : source_par, b: source_par, show : bool = False ) -> None:
        
        super().__init__(a,b)

        FILE_JS_COMPILES = pkg_resources.resource_filename(settings.PACKAGE_NAME, settings.RESOURCE_FILES.FILE_OUTPUT_JS_COMPILED)

        with open(FILE_JS_COMPILES,'r',encoding='utf-8') as f:
            t = f.read()

        class _widget(anywidget.AnyWidget): #type : ignore
            
            _esm = t + """
            function render({ model, el }) {
                let d1 = document.createElement("div"); d1.style.height = '500px'; el.appendChild(d1);
                let d2 = document.createElement("div"); d1.appendChild(d2);
                //console.clear();
                window['m'] = model;
                run({el:d2, e:1, model, inst: """ + str(self.INST) +"""});
                
            } export default { render };
            """       

            _css = """"""
            # value = traitlets.Int(0).tag(sync=True)
            # value : traitlets = traitlets.Int(12).tag(sync=True)
        
        self.widget : _widget = _widget()
        self.widget.on_msg(self._msg_from_widget)
        self.output_msg : Optional[widgets.Output] = None

        if show:
            display(self.widget)            

    def _msg_to_socket(self, msg : Any ) -> None:
        async def send_msgs() -> None:
            for c in FileWidget._WS.get(self.INST,set()):
                try:
                    await c.send(msg)
                except Exception as e: ...
        
        loop = asyncio.get_event_loop() # Obter o loop de eventos atual e executar a função assíncrona
        if loop.is_running():
            asyncio.ensure_future(send_msgs(), loop=loop)
        else:
            loop.run_until_complete(send_msgs())

    def display_msg(self, clear : bool = False) -> None:

        if not self.output_msg:
            self.output_msg = widgets.Output()
        elif clear:
            self.output_msg.clear_output()
        display(self.output_msg)


    def _msg_interna(self, msg: Any, socket0_wdget1 : int) -> None:
        
        CO = settings.COMPILE_OPTIONS #CO.MC_CMD_FORCE_RELOAD
        if type(msg) == str and re.match(f'{CO.MC_CMD_FORCE_RELOAD.value}=.+',msg): #re.findall(f'{CO.MC_CMD_FORCE_RELOAD}=(.*)')
                self._msg_to_socket(msg)
                self.widget.send(msg,None)
        else:
            if self.output_msg:
                with self.output_msg:
                    print(msg)
    
    def _msg_from_socket(self, ws :  WebSocketServerProtocol , msg : Any ) -> None: #msg: str, [str,int], b'text' (mandar Blob)
        self._msg_interna(msg, 0)
    
    def _msg_from_widget(self, w : anywidget.AnyWidget , msg: Any, buffer: Optional[list[memoryview]]) -> None:
        
        try:
            if isinstance(msg,dict) and '_msgid' in msg: #pycall
                rq = cast( NB_REQ, msg )
                req = NB_Request(rq, buffer, lt_log = self.lt)
                resp = route_module(req, NB_Reponse, self.lt)        
                req.jm_send_msg( w, resp )   
        
            else:
                self._msg_interna(msg, 1)
            #w.send({'recebido':c, 'buffer':buffer,'source': 'python', 'msgid_no_reply': c['_msgid']})
        except Exception as e:
            self.lt.append( '\n' + settings.LOG.exception_str(e) + '\n' )
            self.lt.append('msg:erro:'+ str(e))

    
    @staticmethod
    def websocket_init() -> None:
        if FileWidget._WS_PORT: # if settings.WBSOCKET['PORT']:
            return

        def porta_websocket() -> int: #muda por conta do debug, usar porta diferente quando reinicializar o método
            random_number = 0
            while random_number < 1024:
                random_number = secrets.randbelow(10000)
            return random_number

        def run_websocket_server() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            ws_port = porta_websocket()
            FileWidget._WS_PORT = ws_port #settings.WBSOCKET['PORT']        
            start_server = websockets.serve(route_ws, FileWidget._IP_HOST , ws_port)
            loop.run_until_complete(start_server)
            loop.run_forever()

        thread = threading.Thread(target=run_websocket_server)
        thread.start()               

    def flask_server(self) -> None:
        
        lt = settings.DEV_LT
        lt.append('flask server')
        try:
            
            QS = f'?{settings.COMPILE_OPTIONS.FS_QS_ARG_INST.value}={self.INST}'        

            init_ws = False
            if FileWidget._FS is None:
                init_ws = True
                
                #from pkg_resources import resource_stream
                data_path = pkg_resources.resource_filename(settings.PACKAGE_NAME, settings.RESOURCE_FILES.FOLDER_HTML)
                print(data_path)
                # import sys;
                # if sys.version_info >= (3, 9):
                #     import importlib.resources as importlib_resources
                # else:
                #     import importlib_resources
                

                FileWidget._FS = FServer(data_path,host=FileWidget._IP_HOST,route=route_module_flask)

                #ret = nbFlask.fserv(data_path,port,modulo='sys',route=route_module_flask) 
                file = settings.RESOURCE_FILES.FILE_HTML_FOR_JS.replace(settings.RESOURCE_FILES.FOLDER_HTML,'')

            print(f'http://127.0.0.1:{FileWidget._FS.port}{file}{QS}')
            display(FileWidget._FS.button_off)

            if init_ws:
                self.websocket_init()
        except Exception as e:
            lt.append(('fsever error:',e))


        
        # print(f'http://127.0.0.1:{port}/{JMOD}/index.html')
        # print(f'http://127.0.0.1:{port}/{COUT}/main.html')
        # print(f'http://127.0.0.1:{port}/{COUT}/__JS_INSIDE__.html')
        #                 #print(f'http://127.0.0.1:{port}/shutdown')

        

        #ws://localhost:8765




def nb_js_com(py_com : str, js_com : str, array_js_msg : Optional[str] = None ) -> str:
    
    
    SC = r'C:\Users\Christoph Cury\source\2023\ploft\scripts'
    CW = os.getcwd()
    FS = r'C:\Users\Christoph Cury\source\2023\ploft\js_dev\src\models\FoldersExplorer'

    # par_extra = ''
    # if array_js_msg:
    #     par_extra = f',{array_js_msg}'

    ht1 = '''
    <div><div></div></div>
    <div><div id="''' + js_com+ '''"></div><div>
    <script>
        window['goog'] = {'define':function(n,v){ return v;}}
    </script>
    <script type="module">
        import { model_google } from ''' + "'" +  os.path.relpath(FS, CW).replace('\\','/')  + '''/fe_root.js';
        { ''' +  \
            f'let el = document.getElementById("{js_com}");' + \
            f'model_google.view_ffile.run(el,1,["{py_com}","{js_com}"],{array_js_msg}); //0.FULLPAGE, 1.NOTEBOOK' + \
    ''' 
    }</script>'''    
    return ht1  #f'console.log("array visível",{array_js_msg});' + \





def nb_inject_comm_js( target_js : str, afmsg : str ) -> Comm:
    
    #function f_msg(msg){ ''' + afmsg + '''.forEach(f=> f(msg)); }  #console.log('z',m);
    html_cjs = '''<script>var ''' + afmsg + ''' = [];{
            let fm=(m)=>{''' + afmsg + '''.forEach(f=>f(m)); };     
            //''' + afmsg + '''.push((m)=>console.log(m.content.data));
            IPython.notebook.kernel.comm_manager.register_target("''' + target_js + '''",(comm_js,msg)=>{ comm_js.on_msg(fm);});
        }</script>'''
    
    from IPython.display import display
    from IPython.core.display import HTML
    display(HTML(html_cjs))
    return Comm(target_name = target_js )


def route_module_nb() -> Comm:

    target_py, target_js = [f'{x}{datetime.now().strftime("%d%H%M%S%f")}' for x in ['py','js']]
    
    array_js_msg = f'a{target_js}'
    comm_js : Comm = nb_inject_comm_js(target_js, array_js_msg)
    
    #print('cmmjs ab',comm_js)
    #return
    #comm_js.send('abertura2')
    
    #comm_js.send('tody')
    #comm_js : Optional[Comm] = None # = Comm(target_name = target_js )
    #print(comm_js)
    #print(f'a{target_js}')
    #return
    import os
    d = os.__dict__['m'] = []
    j = os.__dict__['j'] = []

    def on_msg(msg : JN_MSG) -> None:
        #display(HTML(f'<script>console.log("{msg}")</script>'))
        
        # nonlocal comm_js
        # comm_js.send({ 'resp':{'recebido': msg['content']['data']}, 'msgid': msg['msg_id'] } )
        # d.append(msg)

        # if msg['content']['data'] == target_js:
        #     #nonlocal comm_js
        #     comm_js = Comm(target_name = target_js ) 
        #     j.append('registrou sim')

        #     #display(HTML('<script>console.log("registrado")</script>'))
        #     return
        
        #2024-06-11
        # jm_req = JN_Request(msg)
        # # j.append(jm_req) #DEBUG

        # # if not jm_req.trusted_hosts:
        # #     return None
        # # jm_req.trusted_hosts.append('rm 0')
        # try:
        #     r = route_module(jm_req,NB_Reponse)        
        #     # jm_req.trusted_hosts.append(('comm',comm_js)) # type: ignore
        #     # jm_req.trusted_hosts.append(('r',r)) # type: ignore
        #     jm_req.jm_send_msg(comm_js, r)
        #         #r._request = jm_req # type: ignore #DEBUG 2024-05-28
                
        # except Exception as e: ...
        #     #jm_req.trusted_hosts.append('except ' + str(e))
        ...


    def on_close(msg : JN_MSG) -> None:
        ...


    def py_reg(comm : Comm, msg : JN_MSG) -> None:
        comm.on_msg(on_msg)
        comm.on_close(on_close)

    get_ipython().kernel.comm_manager.register_target(target_py, py_reg ) # type: ignore    #('plog2', freg)             

    ht1 = nb_js_com(target_py,target_js, array_js_msg)
    from IPython.display import display
    from IPython.core.display import HTML
    display(HTML(ht1))
    return
    print('??',target_js )
    comm_js.send('FInalizado3')
    return comm_js
    #comm_js = Comm(target_name = target_js )
    
    


# def nbx() -> None:
#     target_py, target_js = [ f'{datetime.now().isoformat()}_{x}' for x in ['py','js']]
#     #def step1_reg_pylisten(self) -> None:
#     def on_msg(msg : JN_MSG) -> None:
#         try:
#             data = msg['content']['data']
#             msg_id = data[self._msgid]
#             if msg_id in self.pending_promises:
#                 output, cb = self.pending_promises[msg_id]
#                 if output:
#                     with output:
#                         print(data[self._resp])

#                 if cb:
#                     cb(data[self._resp])

#                 del self.pending_promises[msg_id]        
#         except Exception as e:
#             self.lt_log.append('erro',e)

        
#         def py_reg(comm : Comm, msg : JN_MSG) -> None:
#             comm.on_msg(on_msg)        
#         get_ipython().kernel.comm_manager.register_target(self.target_py, py_reg ) # type: ignore    #('plog2', freg)       






    


