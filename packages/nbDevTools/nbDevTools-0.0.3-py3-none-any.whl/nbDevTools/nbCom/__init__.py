from typing import Callable, Optional, Any

import inspect
from string import Template

from ipykernel.comm import Comm #, CommManager

from IPython.display import  display
from IPython.core.display import HTML

import ipywidgets as widgets
from datetime import datetime

from typing import TypedDict, Callable, Any
from nbDevTools.nbCom.jupyter import JN_MSG, CODEJS

#import asyncio    # problema recebimento mensagem loop jupyter

from typing_extensions import Literal 



def extrair_corpo_funcao( func : Callable[[],Any], inside : bool = False , dic : Optional[dict[str,str]] = None ) -> str:
    
    source_code = inspect.getsource(func)
    lines = source_code.splitlines()
    if inside:
        lines = lines[1:]
    min_indent = min(len(line) - len(line.lstrip(' ')) for line in lines if line.strip())
    stripped_lines = [line[min_indent:] for line in lines]
    cleaned_source_code = "\n".join(stripped_lines)

    if dic:
        cleaned_source_code = Template(cleaned_source_code).safe_substitute(dic)
    
    return cleaned_source_code



# comm.send(data:Any, metadata: Any, buffers: list[memorymap])
# const blob = new Blob([msg.buffers[0]], { type: 'application/octet-stream' });
# const buffer = new Float64Array(msg.buffers[0]); buffer.length , buffer[i] .. 

# import comm_nb; from importlib import reload; comm_nb = reload(comm_nb)
# j = comm_nb.nb_pycback_example()


class nb_pycback_example:
    COMMBACK = Literal['MSG','CLOSE']

    def __init__(self, target_js : str = '' , target_py : str = '' ) -> None:

        self.target_js, self.target_py = target_js, target_py
        if not target_py or not target_js:               
            self.target_py, self.target_js = datetime.now().isoformat() + 'py', datetime.now().isoformat() + 'js'             

        self.i = 0
        self.lt_log : list[Any] = []

        self.cback : dict[nb_pycback_example.COMMBACK, list[Callable[[Any],None]]] = {
            'CLOSE' : [], 'MSG' : []
        }
        self.step1_reg_pylisten() #1o  RECEPTOR PYTHON        
        
        self.comm_js : Comm
        self.step2_display_js()                

        self.step3_set_py_cback()        

    def step1_reg_pylisten(self) -> None:
        def on_msg(msg : Any) -> None:
            self.i += 1
            for fm in self.cback['MSG']:
                fm(msg)
        
        def on_close(msg : JN_MSG) -> None:
            for fc in self.cback['CLOSE']:
                fc(msg)
        
        
        def py_reg(comm : Comm, msg : JN_MSG) -> None:
            self.lt_log.append(('open',msg))
            comm.on_msg(on_msg)
            comm.on_close(on_close)
        
        get_ipython().kernel.comm_manager.register_target(self.target_py, py_reg ) # type: ignore    #('plog2', freg)                

    def step2_display_js(self) -> None:
        html = '''<div id="''' + self.target_js + '''"> <input type="text"></input> <button>RUN</button> </div>
        <script>{  let pcalc = ''' + CODEJS.reg_pycalc_cback(self.target_py,self.target_js) + ''';        
        let i = 0;
        let div = document.getElementById("''' + self.target_js + '''");
        let input = div.querySelector('input');
        let button = div.querySelector('button');
        button.onclick = async (e)=> {
            let value = input.value;
            let r = await pcalc(value,2000);
            console.log(value,'=', r)
        }; }</script>'''
        display(HTML(html))
        self.comm_js = Comm(target_name = self.target_js ) # type: ignore  #sem tipo
    
    def step3_set_py_cback(self) -> None:
        def resp(msg : JN_MSG) -> None:
            mid = msg['msg_id']
            resp = "recebido: " + msg['content']['data']
            self.comm_js.send({ 'msgid':mid, 'resp': resp })
        self.cback['MSG'].append( resp)
        #self.cback['MSG'].append( lambda m: self.lt.append(m))


class nb_jscback_example:
    def __init__(self, target_js : str = '' , target_py : str = '',
                 msgid: str = 'msgid', resp : str = 'resp', data : str = 'data' ) -> None:
        self._msgid , self._resp, self._data = msgid, resp, data
        self.target_js, self.target_py = target_js, target_py
        if not target_py or not target_js:               
            self.target_py, self.target_js = datetime.now().isoformat() + 'py', datetime.now().isoformat() + 'js'             
        
        self.pending_promises : dict[str, tuple[Optional[widgets.Output], Optional[Callable[[Any],None]] ]]= {}     

        self.o = widgets.Output()
        self.step1_reg_pylisten()
        self.lt_log : list[Any] = []

        #1
        html = '''<script>{
            console.log(1,"''' +  self.target_js +'''");
            let cm = Jupyter.notebook.kernel.comm_manager;
            let comm_py = cm.new_comm("''' + self.target_py + '''",null);
            cm.register_target("''' +  self.target_js +'''", function(comm_js) {
                comm_js.on_msg(function(msg) {
                    console.log('recebido msg',msg);
                    const data = msg.content.data;
                    const result = performSomeCalculation(data.''' +  self._data +''');
                    let obj = {''' +  self._msgid +''': data.''' +  self._msgid +''', ''' +  self._resp +''': result};
                    console.log(obj);
                    let z = comm_py.send(obj);
                    console.log('enviado', z);
                });
            });

            function performSomeCalculation(input) {
                let resp =  input + " processed!";
                console.log(input,'=',resp);
                return resp;
            }
        }</script>'''     
        display(HTML(html))
        self.comm_js = Comm(target_name = self.target_js ) # type: ignore  #sem tipo

    def step1_reg_pylisten(self) -> None:
        def on_msg(msg : JN_MSG) -> None:
            try:
                data = msg['content']['data']
                msg_id = data[self._msgid]
                if msg_id in self.pending_promises:
                    output, cb = self.pending_promises[msg_id]
                    if output:
                        with output:
                            print(data[self._resp])

                    if cb:
                        cb(data[self._resp])

                    del self.pending_promises[msg_id]        
            except Exception as e:
                self.lt_log.append(('erro',e))

        
        def py_reg(comm : Comm, msg : JN_MSG) -> None:
            comm.on_msg(on_msg)        
        get_ipython().kernel.comm_manager.register_target(self.target_py, py_reg ) # type: ignore    #('plog2', freg)          

    
    def calc(self, data : Any , *, bprint : bool = True, cb : Optional[Callable[[Any], None]] = None ) -> None:
        
        output : Optional[widgets.Output] = None
        if bprint:
            output = widgets.Output()
            self.o = output
            display(output)
        
        msg_id = str(id(data))  # Simple way to generate a unique ID for the message
        self.comm_js.send({ self._data: data, self._msgid: msg_id})
        self.pending_promises[msg_id] = (output,cb)


__all__ = ['JN_MSG']