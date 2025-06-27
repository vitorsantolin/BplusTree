from collections import deque
class Node:
    def eh_folha(self):
        return False

class LeafNode:
    def __init__(self, ordem):
        self.ordem = ordem
        self.chaves = []
        self.valores = []
        self.proximo = None  # Próxima folha
        self.anterior = None # previu
        self.pai = None

    def eh_folha(self):
        return True
    def __str__(self):
        return f"Nófolha(chaves={self.chaves}, valores={self.valores})"
    def is_cheio(self):
        return len(self.chaves) >= self.ordem -1
    def vazio(self):
        return len(self.chaves) == 0
    def eh_folha(self):
        return True
    

class InternalNode:
    def __init__(self, ordem):
        self.ordem = ordem
        self.filho = []
        self.pai = None
        self.chaves = []
    def eh_folha(self):
        return False
    def is_cheio(self):
        return len(self.chaves) > self.ordem
    def __str__(self):
        return f"Nóinterno(chaves={self.chaves}, contafilho={len(self.filho)})"

class BPlusTree:
    def __init__(self, ordem):
        self.ordem = ordem
        self.raiz = LeafNode(ordem)
    def buscar(self, chave):
        current_node =self.raiz
        while not current_node.eh_folha():
            node_chaves = current_node.chaves
            index = 0
            for i in range(len(node_chaves)):
                if chave < node_chaves[i]:
                    index = i 
                    break
                else:
                    index += 1
            current_node = current_node.filho[index]
        return current_node
    
    def buscar_folha(self, chave):
        leaf = self.buscar(chave)
        for i in range(len(leaf.chaves)):#vai fazer a busca nas folhas
            if leaf.chaves[i] == chave:
                return leaf.valores[i]

        #caso n seja encontrado vai percorrer até o possivel lugar de deveria estar
        # isso de forma logN e caso n estiver vai retornar que n tem 
        return None
    
    def insert(self, chave, valor):#Vai inserir dentro da arvore
        leaf = self.buscar(chave) #encontrar o local certro atraves da busca
        self.insert_folha(leaf, chave, valor)#insere com base na ordem 
        if len(leaf.chaves) == self.ordem: # verefica a ordem
            new_leaf = LeafNode(self.ordem)
            metade = len(leaf.chaves) // 2  #através da função para split faz o caluclo
            new_leaf.chaves = leaf.chaves[metade:]
            new_leaf.valores = leaf.valores[metade:]#faz a divisão
            new_leaf.pai = leaf.pai
            leaf.chaves = leaf.chaves[:metade]
            leaf.valores = leaf.valores[:metade]
            new_leaf.proximo = leaf.proximo
            new_leaf.anterior = leaf
            if leaf.proximo:
                leaf.proximo.anterior = new_leaf
            leaf.proximo = new_leaf

            self.insert_pai(leaf, new_leaf.chaves[0], new_leaf)

    def insert_folha(self, leaf, chave, valor):
        #insere na folha pos busca
        if leaf.chaves: 
            for i in range(len(leaf.chaves)):
                if chave == leaf.chaves[i]:
                    leaf.valores[i] = valor 
                    return
                elif chave < leaf.chaves[i]:#insere a chave  e valor na posição correta
                    leaf.chaves.insert(i, chave) 
                    leaf.valores.insert(
                        i, valor
                    )  
                    return
           #após adiviona o valor e chave
            leaf.chaves.append(chave)
            leaf.valores.append(valor)
        else:  
            leaf.chaves = [chave]
            leaf.valores = [valor]
        
    def insert_pai(self, node_atual, chave, novo_node):
        
      # caso for na raiz 
        if node_atual.pai is None:
            nova_raiz = InternalNode(self.ordem)
            nova_raiz.chaves = [chave]
            nova_raiz.filho = [node_atual, novo_node]
            self.raiz = nova_raiz
            node_atual.pai = nova_raiz
            novo_node.pai = nova_raiz
            return
        # inserir no pai 
        pai = node_atual.pai
        novo_node.pai = pai
        #procura  aposição certa para inserir
        for i in range(len(pai.filho)):
            if pai.filho[i] == node_atual:
                pai.chave.insert(i, chave)
                pai.filho.insert(i + 1, novo_node)
                break

       # se ao inserir tiver estourando ou seja igual a ordem determinada
        if len(pai.keys) == self.ordem:
            novo_pai = InternalNode(self.ordem)
            novo_pai.pai = pai.pai
            metade = len(pai.keys) // 2  
            promoted_key = pai.keys[metade]
            novo_pai.chaves = pai.chaves[metade + 1 :]
            novo_pai.filho = pai.filho[metade + 1 :]
            pai.keys = pai.chaves[:metade]
            pai.filho = pai.filho[: metade + 1]
           #apos inserir ele tem que autlaizar
            for folha in novo_pai.filho:
                folha.pai = novo_pai

            self.insert_pai(pai, promoted_key, novo_pai)

    def remover(self, chave):
        #assim como na inserção , é necessario fazer a busca do elemento para remover 
        leaf = self.buscar(chave)
        if chave not in leaf.chaves:
            return None
        index = leaf.chaves.index(chave)
        leaf.chaves.pop(index)
        leaf.valores.pop(index)
        #se tiver na raiz, ele ja retorno , pois n tem nada
        if leaf is self.raiz:  
            return
        if len(leaf.chaves) >= self.minimo_filho_no():
            self.chave_pai_fixa(leaf)
            return
        self.remover_entrada(leaf)

    def minimo_filho_no(self):
        #quantidade chaves pós exclusão em folha
        return self.ordem // 2
    def minimo_chavesdentro(self):
        #quantidade chaves pós exclusão em um node
        return (self.ordem - 1) // 2
    def minimo_chaves(self, node):
        #minimo para o nó 
        return (
            self.minimo_filho_no()
            if node.eh_folha()
            else self.minimo_chavesdentro()
        )
    def remover_entrada(self, node):
        pai = node.pai
        if pai is None:
            if (not node.is_leaf()) and len(node.filho) == 1:
                self.raiz = node.filho[0]
                self.raiz.pai = None
            return
        pos = pai.filho.index(node)
        esquerda = pai.filho[pos - 1] if pos > 0 else None
        direita = pai.filho[pos + 1] if pos < len(pai.filho) - 1 else None

       #balancear a esquerda
        if esquerda and len(esquerda.chaves) > self.minimo_chaves(esquerda):
            self.pegar_esquerda(node, esquerda, pai, pos - 1)
            return

        #balancear a direita
        if direita and len(direita.minimo_chaves) > self.minimo_chaves(direita):
            self.pegar_direita(node, direita, pai, pos)
            return
        if esquerda:
            self.alterna_nodes(esquerda, node, pai, pos - 1)
            paiafetado = pai
        else:
            self.alterna_nodes(node, direita, pai, pos)
            paiafetado = pai
        if paiafetado is self.raiz and len(paiafetado.chaves) == 0:
            self.raiz = paiafetado.filho[0]
            self.raiz.pai = None
        elif len(paiafetado.chaves) < self.minimo_chavesdentro():
            self.remover_entrada(paiafetado)

    def fixar_chave_pai(self, node):
        pai = node.pai #atualiza o pai quando a chave de uma folha mudar
        if not pai or not node.chaves:
            return
        pos = pai.filho.index(node)
        if pos > 0:
            pai.chaves[pos - 1] = node.chaves[0]
            self.fixar_chave_pai(pai)
        
    def pegar_esquerda(self, node, left, pai, sep_idex):
        if node.is_leaf():#move para esquerda
            node.chaves.insert(0, left.chaves.pop(-1))
            node.valores.insert(0, left.valores.pop(-1))
            pai.chaves[sep_idex] = node.chaves[0]
        else:
            sep_chave = pai.chaves[sep_idex]
            filho1 = left.filho.pop(-1)
            node.filho.insert(0, filho1)
            filho1.pai = node
            node.chaves.insert(0, sep_chave)
            pai.chaves[sep_idex] = left.chaves.pop(-1)

    def pegar_direita(self, node, direita, pai, sep_idex):
        if node.is_leaf():#move para direita
            node.chaves.append(direita.chaves.pop(0))
            node.valores.append(direita.valores.pop(0))
            pai.chaves[sep_idex] = direita.chaves[0]
        else:
            sep_key = pai.chaves[sep_idex]
            filho1 = direita.filho.pop(0)
            node.filho.append(filho1)
            filho1.pai = node
            node.chaves.append(sep_key)
            pai.chaves[sep_idex] = direita.chaves.pop(0)
        
    def alterna_nodes(self, esquerda, direita, pai, sep_idex):
        if esquerda.eh_folha():
            esquerda.chaves.extend(direita.chaves)
            esquerda.valores.extend(direita.valores)
            esquerda.proximo = direita.proximo
            if direita.proximo:
                direita.proximo.anterior = esquerda
        else:
            saparador = pai.chaves[sep_idex]  # separator - key between the siblings
            esquerda.chaves.append(saparador)  # bring separator down into left node
            esquerda.chaves.extend(direita.chaves)
            for child in direita.filho:
                child.pai = esquerda
            esquerda.filho.extend(direita.filho)
        pai.chaves.pop(sep_idex)
        pai.filho.pop(sep_idex + 1)

    def pegar_todas_chaves(self):
        chaves = []
        #encontra a primeira folha
        current_leaf = self.raiz
        while isinstance(current_leaf, InternalNode):
            current_leaf = current_leaf.filho[0]  #pega o ultimo da esquerda

        while current_leaf: #pecore as folha na lista encadeada
            for k in current_leaf.chaves:
                chaves.append(k)
            current_leaf = (
                current_leaf.proximo
            )  

        return chaves

       