class Locker:
  def __init__(self):
      self.ocupado = False
      self.senha = None
      self.produto = None

  def liberar(self):
      self.ocupado = False
      self.senha = None
      self.produto = None

  def ocupar(self, produto, senha):
      self.ocupado = True
      self.produto = produto
      self.senha = senha


class Apartamento:
  def __init__(self, numero, morador, senha):
      self.numero = numero
      self.morador = morador
      self.locker = Locker()
      self.locker.senha = senha  # Define a senha ao criar o apartamento

  def __str__(self):
      return f"Apartamento {self.numero}, Morador: {self.morador}, Senha do Locker: {self.locker.senha}"


apartamentos = []


def criapredio():
  numero = input("Digite o número do apartamento: ")
  morador = input("Digite o nome do morador: ")
  senha = input("Digite a senha para o locker do apartamento: ")

  # Verificar se o apartamento já existe
  if any(ap.numero == numero for ap in apartamentos):
      print("Apartamento já existe!")
  else:
      apartamento = Apartamento(numero, morador, senha)
      apartamentos.append(apartamento)
      print(f"Apartamento {numero} cadastrado com sucesso!")


def entrega():
  numero = input("Digite o número do apartamento para entrega: ")
  apartamento = next((ap for ap in apartamentos if ap.numero == numero), None)
  if apartamento:
      produto = input("Digite o nome do produto: ")
      apartamento.locker.ocupar(produto, apartamento.locker.senha)
      print(f"Produto '{produto}' entregue no locker do apartamento {numero}. Senha: {apartamento.locker.senha}")
  else:
      print("Apartamento não encontrado.")


def status_locker():
  numero = input("Digite o número do apartamento para verificar o status do locker: ")
  apartamento = next((ap for ap in apartamentos if ap.numero == numero), None)
  if apartamento:
      if apartamento.locker.ocupado:
          print(f"Locker ocupado. Produto: {apartamento.locker.produto} | Senha: {apartamento.locker.senha}")
      else:
          print("Locker disponível.")
  else:
      print("Apartamento não encontrado.")


def status_apartamento():
  if apartamentos:
      print("\nApartamentos cadastrados:")
      for apartamento in apartamentos:
          print(apartamento)  # Chama o método __str__ da classe Apartamento
  else:
      print("Nenhum apartamento cadastrado.")


def retirar_produto():
  numero = input("Digite o número do apartamento para retirar o produto: ")
  senha = input("Digite a senha do locker: ")
  apartamento = next((ap for ap in apartamentos if ap.numero == numero), None)
  if apartamento and apartamento.locker.senha == senha:
      apartamento.locker.liberar()
      print(f"Produto retirado com sucesso do apartamento {numero}. Locker liberado.")
  else:
      print("Dados inválidos. Verifique o número do apartamento ou a senha.")


def menu():
  print("\nMenu:")
  print("1 - Sair do aplicativo")
  print("2 - Realizar Entrega")
  print("3 - Status do Locker")
  print("4 - Status do Apartamento")
  print("5 - Cadastro de novo apartamento, morador e locker")
  print("6 - Retirar produto")


# Menu principal
while True:
  menu()
  entrada = -1
  while entrada <= 1 or entrada >= 7:
      try:
          entrada = int(input("Escolha uma opção: "))
          break
      except ValueError:
          print("Digite uma opção válida.")

  if entrada == 1:
      print("Saindo do aplicativo...")
      break
  elif entrada == 2:
      entrega()
  elif entrada == 3:
      status_locker()
  elif entrada == 4:
      status_apartamento()
  elif entrada == 5:
      criapredio()
  elif entrada == 6:
      retirar_produto()
