from typing import Callable,  Optional
import os

import pathlib


def modificar_e_gravar_arquivo(source_file : str, target_file : str , *, 
                               pairs : list[tuple[str,str]], fedit : Optional[Callable[[str],str]] = None  ) -> None:
    try:
        # Abrir o arquivo de origem para leitura
        with open(source_file, 'r', encoding='utf-8') as origem:
            conteudo = origem.read()

        for busca, substituicao in pairs:
            conteudo = conteudo.replace(busca, substituicao)     

        if fedit:
            conteudo = fedit(conteudo)
            #lambda x : f'export const JS_CODE = `\n{x}\n`'   
            #conteudo = f'export const JS_CODE = `\n{conteudo}\n`'   

        with open(target_file, 'w', encoding='utf-8') as destino:
            destino.write(conteudo)
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

class path:

    @staticmethod
    def upto(up_folder:str, from_folder : Optional[str] = None ) -> str:
        if from_folder is None:
            from_folder = os.getcwd()

        #print(from_folder, up_folder)

        for parent in pathlib.Path(from_folder).parents:
            if parent.name == up_folder:
                return str(parent)
        
        #lt = from_folder.split(os.sep)
        #n = len(lt)
        #try:
        #    while lt[n-1] != up_folder:
        #        n-=1
        #    return os.sep.join(lt[0:n])
        raise RuntimeError(f'Pasta não encntrada {up_folder} acima de {from_folder} ')


    @staticmethod
    def relative_to(from_folder:str, to_folder:str) ->str:
        return str(pathlib.Path(to_folder).relative_to(pathlib.Path(from_folder)))
    
    @staticmethod
    def relpath(from_folder: str, to_folder: str) -> str:
        """
        Calcula o caminho relativo de from_folder para to_folder,
        tratando os casos de subida e descida de diretórios.
        Retorna uma string vazia se os diretórios forem os mesmos.
        """
        rel_path = os.path.relpath(to_folder, start=from_folder)
        return rel_path if rel_path != '.' else ''




'''

do jupyter notebook - ver local do arquivo que roda o script
get_ipython().starting_dir

'''