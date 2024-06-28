from typing import TypedDict, Callable, Any
import re

from typing import TypedDict, Callable, Protocol, Any, Optional, Type, Union, Mapping, cast
from enum import Enum

from werkzeug.datastructures import MultiDict, ImmutableMultiDict, FileStorage, Headers
from werkzeug.utils import cached_property

from ipykernel.comm import Comm #, CommManager
from enum import IntEnum
import io

from werkzeug.utils import cached_property
#from werkzeug.wrappers import FileStorage
from urllib.parse import urlparse, parse_qs
import base64
import json


#NOTEBOOK - REQ
# class NB_REQ{
#     constructor(){
#         /** @type {*} @export */ this.content; //para manter nome dos parâmetros precisa estar em cada um
#         /** @type {!Array.<!ArrayBuffer>} @export */this.buffer;
#         /** @type {string} @export */ this._msgid;
#         /** @type {string} @export */ this.url;                
#         /** @type {!FormData} @export */ this.form;
#         /** @type {string} @export */ this.method;        
#         /** @type {string} @export */ this.mimetype;
#         /** @type {!Object.<string,string>} @export */ this.headers;
#         /** @type {!rtype} @export */ this._rtype;
#     }
# }

class NB_RTYPE(IntEnum):
    undefined = 0
    json = 1
    blob = 2
    text = 3

JSONType = Union[str, int, float, bool, None, dict[str, 'JSONType'], list['JSONType']]

class NB_REQ(TypedDict, total = False):
    content : Any
    buffer : list[memoryview]
    _msgid : str
    url : str
    form : dict[str,str] #'application/x-www-form-urlencoded' tudo string,  'multipart/form-data' string e binário
    #json : JSONType
    method : str
    #mimetype : str
    headers : Mapping[str,str]
    _rtype : NB_RTYPE




class JN_MSG_Content(TypedDict, total = False):
    ename: str #error
    evalue: str
    traceback : list[str]    
    data : Any #execute_result / display_data / #comm_msg  -  @type {{'text/plain': string, 'text/html': string}} 
    execution_count : int #execute_result      
    name : str #stream
    text : str


class JN_MSG_Header(TypedDict): #, total = False
    date : str
    msg_id : str
    msg_type : str
    session: str
    username : str
    version : str

class JN_MSG(TypedDict): #, total = False
    content : JN_MSG_Content
    channel : str
    buffers : list[memoryview]
    header : JN_MSG_Header
    msg_id : str
    msg_type : str


class IRequest(Protocol):

    @cached_property
    def args(self) -> MultiDict[str, str]: ...
    @cached_property
    def form(self) -> ImmutableMultiDict[str, str]: ...
    @cached_property
    def files(self) -> ImmutableMultiDict[str, FileStorage]: ...

    headers : Headers

    @cached_property
    def full_path(self) -> str: ...
    #trusted_hosts : Optional[list[str]]
    method : str
    path : str
    def get_json(self, force: bool = False, silent: bool = False, cache: bool = True) -> Any: ...

class IResponse(Protocol):
    #_request : Any
    def __init__(self, 
        response: Optional[Union[bytes, str]] = None, 
        status : Optional[int] = None, 
        mimetype : Optional[str] = None,
        headers : Optional[Mapping[str,str]] = None  #(parameter) headers: Mapping[str, str | int | Iterable[str | int]] | Iterable[Tuple[str, str | int]] | None
        ) -> None: ...
TResponse = Type[IResponse]

#NB-JAVASCRIPT - PADRÕES COMUNICAÇÃO 

ARRAYBUFFER_POS : list[str] = ['arrayBuffer_pos','_type_'] #'arrayBuffer-pos'

# class rtype(IntEnum):
#     json = 0
#     blob = 1
#     text = 2
#     undefined = 3

# class RequestInit(TypedDict, total = False):
#         headers : dict[str,str]
#         method : str
#         body : Any #Blob | BufferSource | FormData | URLSearchParams | string;

# class NB_MSG_DATA(TypedDict, total = False):
#     url : str
#     options : RequestInit
#     ret :  rtype

class NB_RESP(TypedDict, total = False):
    _msgid : str
    #resp : Any
    response : Union[bytes, str, None]
    status : int
    # mimetype : str
    headers : Mapping[str,str]


class NB_Request: #ESTILO FLASK
    
    def __init__(self, c : NB_REQ, buffer: Optional[list[memoryview]], *, lt_log : list[Any] = []) -> None:
        self._req : NB_REQ = c
        self._buff : Optional[list[memoryview]] = buffer
        
        self.lt_log = lt_log
        self.lt_log.append('NB_Request init:')
        # self.lt_log.append(self.__dict__)
        self.lt_log.append({'req': self._req.keys(), 'buf': self._buff})

        

        self.method = c.get('method','GET')
        self._parsed_url = urlparse(c.get('url',''))
        self.path = self._parsed_url.path
        
        self._form : dict[str,str] = {}
        self._files : dict[str,FileStorage] = {}

        
        self.headers : Headers = Headers()
        for k,v in c.get('headers',{}).items():
            self.headers.add(k,v)        

        pattern = f'^{re.escape(ARRAYBUFFER_POS[0])}(\\d+){re.escape(ARRAYBUFFER_POS[1])}([^ ]+)$'


        
        for k,v in self._req.get('form',{}).items():

            match = re.search(pattern, v)
            if match:
                lt_log.append(f'form match {(match[1], match[2])}' )
                
                i = int(match[1])
                if buffer and len(buffer) > i:
                    file_stream = io.BytesIO(buffer[i])
                    self._files[k] = FileStorage(stream=file_stream,content_type= match[2]) #filename='example.txt',content_type='text/plain'
                else:
                    raise ValueError(f'buffer ={type(buffer)} len={ len(buffer) if buffer else "nd"}, i= {i}')
            else:
                self._form[k] = v

        self.lt_log.append({'req':self._req, 'form':self._form, 'files':self._files})


    @cached_property
    def args(self) -> MultiDict[str, str]:
        query_params = parse_qs(self._parsed_url.query)
        return MultiDict({k: v[0] for k, v in query_params.items()})
            
    @cached_property
    def form(self) -> ImmutableMultiDict[str, str]:
        #tipos que conteúdo é form 'application/x-www-form-urlencoded' 'multipart/form-data'
        # atualmente só estou passando por formData pra form, não vem nada pelo content  
        return ImmutableMultiDict(self._form)
    @cached_property
    def files(self) -> ImmutableMultiDict[str, FileStorage]:
        return ImmutableMultiDict(self._files)

    @cached_property
    def full_path(self) -> str:
        return self.path + ('?' + self._parsed_url.query if self._parsed_url.query else '')
    
    method : str
    path : str
    def get_json(self, force: bool = False, silent: bool = False, cache: bool = True) -> Any:
        header = self._req.get('headers',{})
        mimetype = header.get('Content-Type','')
        
        self.lt_log.append(f'NB_Request gjson {header}')

        if mimetype == 'application/json':
            sload = self._req.get('content','')
            self.lt_log.append(f'jsload type {type(sload)}  {sload}')
            return json.loads(sload)
        
        self.lt_log.append('json não é mime, None')
        

    def __repr__(self) -> str:
        return f'NB_Rquest:\n{self._req}'
    
    def jm_send_msg( self, com : Comm, resp : Optional[IResponse] ) -> None: 
        
        msgid = self._req.get('_msgid','')
        erro_text = ''
        if isinstance(resp,NB_Reponse):
            resp.data['_msgid'] = msgid
            #resp.data[]
            self.lt_log.append(f'type resp.contnt = {type(resp.data)}')
            self.lt_log.append(f'contnt = {resp.data}')
            #self.lt_log.append(('resp=',resp.data))

            data_response = resp.data.get('response')
            if type(data_response) == str or data_response is None:
                com.send(resp.data,[])
                return None #OK
            else:
                buff : Optional[memoryview] = None            
                try:
                    buff = memoryview(data_response) #type: ignore
                except Exception as e:
                    erro_text = f'{e} type={type(data_response)}'

                if buff:
                    resp.data['response'] = None
                    com.send(resp.data, [buff])
                    return None #OK

        #ERRO / FORMATO INVÁLIDO
        nr : NB_RESP = { '_msgid': msgid, 'status': 500 ,'response':erro_text, 'headers': {'Content-Type': 'text/plain' } }
        com.send(nr)




class NB_Reponse:
    def __init__(self, 
        response: Optional[Union[bytes, str]] = None, 
        status : Optional[int] = None, 
        mimetype : Optional[str] = None,
        headers : Optional[Mapping[str,str]] = None  #(parameter) headers: Mapping[str, str | int | Iterable[str | int]] | Iterable[Tuple[str, str | int]] | None
        ) -> None:
            self.data : NB_RESP = {}
            if response:
                self.data['response'] = response
            if status:
                self.data['status'] = status
            if headers:
                self.data['headers'] = headers
            if mimetype:
                self.data['headers'] =  {'Content-Type': mimetype } 

        

class CODEJS:

    @staticmethod
    def reg_pycalc_cback(py_target : str, js_target : str, 
                          par_msgid:str = 'msgid', par_resp :str = 'resp',var_pending :str = 'p' ,
                          jscode_error_timeout : str = 'new Error("Timeout")') -> str:
        code = '''(()=>{
                let cm = IPython.notebook.kernel.comm_manager;
                let comm_py = cm.new_comm("''' + py_target + '''",'');
                
                let ''' + var_pending + ''' = {}; 
                cm.register_target("''' + js_target + '''",(comm_js,msg)=>{
                    comm_js.on_msg(msg=>{
                        let cdata = msg.content.data;
                        if (''' + var_pending + '''[cdata?.''' + par_msgid + ''' ?? null]) {
                            ''' + var_pending + '''[cdata.''' + par_msgid + '''].resolve( cdata.''' + par_resp + ''');
                            delete ''' + var_pending + '''[cdata.msgid];
                        }  
                    });
                });
                return async function(x, tout = 5000 ){
                    let msg_id = comm_py.send(x);
                    return new Promise((resolve, reject) => {
                        ''' + var_pending + '''[msg_id] = { resolve, reject };
                        setTimeout(() => {
                            if (''' + var_pending + '''[msg_id]) { reject(''' + jscode_error_timeout + '''); delete ''' + var_pending + '''[msg_id]; }
                        }, tout );
                    });            
                };
            })();                
        '''
        compressed_code = re.sub(r'\s+', ' ', code).strip()
        #formatted_code = re.sub(r' {2,}', ' ', compressed_code)  # Reduz múltiplos espaços para um único espaço
        return compressed_code


# class JN_Request:
    
#     def __init__(self, msg : JN_MSG) -> None:
#         self._md  = cast(NB_REQ, msg['content']['data'] )        
#         self._md['_msgid'] = msg['msg_id'] # pelo comm mensagem é mais 'low level'
        
#         self.method = self._md.get('method','GET')
#         self._parsed_url = urlparse(self._md.get('url',''))
#         self.path = self._parsed_url.path
        
        
#         import os
#         reqs : list[list[Any]] = os.__dict__.get('reqs',[])
#         self.trusted_hosts : Optional[list[str]] = [ ]

#         reqs.append(self.trusted_hosts)
#         os.__dict__['reqs'] = reqs
        
#         self.trusted_hosts.append(str(self._md))

#     @cached_property
#     def args(self) -> MultiDict[str, str]:
#         parsed_url = urlparse(self._md['url'])
#         query_params = parse_qs(parsed_url.query)
#         return MultiDict({k: v[0] for k, v in query_params.items()})
            
#     @cached_property
#     def form(self) -> ImmutableMultiDict[str, str]:
#         d = self._md.get('form',{})        
#         return ImmutableMultiDict(d)
#     @cached_property
#     def files(self) -> ImmutableMultiDict[str, FileStorage]:
#         return ImmutableMultiDict({})

#     @cached_property
#     def full_path(self) -> str:
#         return self.path + ('?' + self._parsed_url.query if self._parsed_url.query else '')
    
#     method : str
#     path : str
#     def get_json(self, force: bool = False, silent: bool = False, cache: bool = True) -> Any:
#         file = r'C:\Users\Christoph Cury\source\2023\ploft\src\filesync\debug.txt'
#         def w(f: Any) -> None:
#             with open(file,'a') as f:
#                 f.write(f'\n{f}')
        
#         w(f'get_json raw {self._md}')
#         js_temp : JSONType =  self._md.get('form',{})  # type : ignore
#         w(f'do form {js_temp}')
#         js_temp = self._md.get('json',js_temp)
#         w(f'ret json {js_temp}')
#         return js_temp

        
    
#     def __repr__(self) -> str:
#         return f'JN_Rquest:\n{self._md}'
    
#     def jm_send_msg( self, com : Comm, resp : Optional[IResponse] ) -> None: 
        
#         if isinstance(resp,NB_Reponse):
#             resp.data['_msgid'] = self._md['_msgid']
#             com.send(resp.data)
#         else:
#             dr : NB_RESP = { '_msgid': self._md['_msgid'], 'status': 500 }
#             com.send(dr)
