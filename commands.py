from arvore_bplus import BPlusTree


class VirtualFileSystem:
    def __init__(self, order=4):
        self.tree = BPlusTree(order)
        self.cwd = "/"
        self.tree.insert("/", {"type": "dir"})



    def mkdir(self, name: str) -> str:
        path = self._full_path(name)
        if self.tree.buscar_folha(path):
            return f"Diretório '{name}' já existe"
        
        self.tree.insert(path, {"type": "dir"})
        return f"Diretório '{name}' criado"




    def touch(self, name: str) -> str:
        path = self._full_path(name)
        if self.tree.buscar_folha(path):
            return f"Arquivo '{name}' já existe"
        
        self.tree.insert(path, {"type": "file"})
        return f"Arquivo '{name}' criado"
    


    def ls(self, path: str = None) -> str:
        path = self.cwd if not path else self._full_path(path)
        node = self.tree.buscar(path)
        
        if not node:
            return f"Diretório '{path}' não encontrado"
        
        if hasattr(node, "chaves"):

            return " ".join(str(k) for k in node.chaves) if node.chaves else "[vazio]"
    
        return "[Tipo de nó desconhecido]"

    def rm(self, name: str) -> str:
        path = self._full_path(name)
        if self.tree.buscar_folha(path):
            self.tree.remover(path)
            return f"'{name}' deletado"
        return f"'{name}' não encontrado"



    def cd(self, path: str) -> str:
        if path == "..":
            if self.cwd == "/":
                return "Já está no diretório raiz"
            
            self.cwd = "/".join(self.cwd.rstrip("/").split("/")[:-1]) or "/"
            return f"Movido para {self.cwd}"

        destino = self._full_path(path)
        val = self.tree.buscar_folha(destino)

        if val and val.get("type") == "dir":
            self.cwd = destino
            return f"Movido para {destino}"
        return f"Diretório '{path}' não encontrado"
    

   
    
    def _full_path(self, name: str) -> str:
        name = name.rstrip("/")
        if name.startswith("/"):
            return name
        return f"{self.cwd.rstrip('/')}/{name}" if self.cwd != "/" else f"/{name}"
