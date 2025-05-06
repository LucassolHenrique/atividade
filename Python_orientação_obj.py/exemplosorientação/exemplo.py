
# Você deverá criar um sistema de locker de entrega de produtos.
# Lógica: O entregador realiza a entrega de um produto escolhendo a opção ENTREGA.
#
#Função def Entrega()
#
#
#
#               Informa o tamanho do pacote, o apartamento e finaliza a entrega. O sistema envia uma mensagem ao nome do apartamento cadastrado com uma senha gerada aleatóriamente.
#
#.             O morador, ao retirar o produto, informa o apartamento e a senha, o locker "Abre". O morador Finaliza a retirada e o locker é liberado.
#
#.             Em configurações deve existir uma opção de cadastro, onde o usuário irá cadastrar o apartamento e uma senha para utilizar o locker.


class Objeto:

    def __init__(self, peso):
        self.peso = peso

class Locker:

    def __ini__(self, peso):
        self.peso = peso


class Apartamento:  #cadastro do locker, apartamento numero e morador.

    def __init__(self, numero):
        self._numero = numero  #atributo protegido

    @property
    def numero(self):
        return self._numero

    def __str__(self):
        return f"apartamento: {self._numero}"


def criapredio(): #deve criar um predio colocar ele a lista de predios e não deixar o usuario colocar um prédio com o mesmo numero





def menu():  #print da tela inicial
    print("1 - saida do aplicativo")
    print("2 - Entrega")
    print("3 - status locker")
    print("4 - status apartamento")
    print("5 - cadastro novo apartamento, morador e locker")
    print("6 - ")


#menu
while True:
    menu()
    entrada = -1
    while entrada <= 1 or entrada >= 6:
        try:
            entrada = int(input("qual Opção"))
            break
        except ValueError:
            print("digite sua opção")
    if entrada == 1:
        break
    elif entrada == 2:

    elif entrada == 3:

    elif entrada == 4:

    elif entrada == 5:

    else entrada == 6:

