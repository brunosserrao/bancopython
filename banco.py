# coding: utf-8
import os
import ast
import datetime

contas = []

#Class Cliente
class Cliente():
	nome = ""
	telefone = ""

	def __init__(self, nome, telefone):
		self.nome = nome
		self.nome = telefone

	def getNome(self):
		return self.nome
	
	def getTelefone(self):
		return self.telefone

#Class Conta: Cliente
class Conta(Cliente):
	cliente = None
	numero = 0
	saldo = 0.0
	especial = False
	historico = [];

	def __init__ (self, cliente, numero, saldo):
		self.cliente = cliente
		self.numero = numero
		self.saldo = saldo
		self.registar_historico(
			{
				"acao": "Criação da Conta",
				"valor": saldo
			}
		)
		 
	def depositar (self, valor):
		self.saldo += valor

		self.registar_historico(
			{
				"acao": "Depósito na Conta",
				"valor": valor
			}
		)
		 
	def sacar (self, valor):
		if (self.saldo >= valor):
			self.saldo -= valor

			self.registar_historico(
				{
					"acao": "Saque na Conta",
					"valor": valor
				}
			)

			return True
		else:
			self.registar_historico(
				{
					"acao": "Saque na Conta: VALOR Insuficiente",
					"valor": valor
				}
			)
			
			return False

	def registar_historico(self, acoes):
		self.historico.append(
			{
				"numero": self.numero,
				"data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				"acao": acoes['acao'],
				"valor": acoes['valor']
			}
		)

	def imprimir_cliente(self):
		print "\n-----------  CLIENTE -------------"
		print "Cliente: {0}".format(self.cliente.getNome())
		print "Telefone: {0}".format(self.cliente.getTelefone())
		print "-----------------------------------"

	def imprimir_conta(self):
		print "\n------------  CONTA -------------"
		print "Conta: {0}".format(self.numero)
		print "Especial: {0}".format(self.especial == True and "Sim" or "Não")
		print "-----------------------------------"

	def imprimir_historico(self):
		print "\n------------ EXTRATO -------------"
		
		for historico in self.historico:
			if int(historico['numero']) == int(self.numero):
				print "{0} - {1} - {2}".format(historico['data'], historico['acao'], historico['valor'])

		print "\nSALDO ATUAL : {0}".format(self.saldo)

		if self.especial:
			print "\nSALDO ESPECIAL : {0}".format(self.limite)

#Cadastrar conta Especial: Conta
class ContaEspecial (Conta):
	limite = 0
	 
	def __init__(self, cliente, numero, saldo, limite):
		self.cliente = cliente
		self.numero = numero
		self.saldo = saldo
		self.limite = limite
		self.especial = True

		self.registar_historico(
			{
				"acao": "Criação da Conta Especial",
				"valor": saldo
			}
		)

	def saqueEspecial(self, valor):
		if (self.saldo + self.limite >= valor):
			self.saldo -= valor

			self.registar_historico(
				{
					"acao": "Saque na Conta Especial dentro do limite de crédito",
					"valor": valor
				}
			)

			return True
		else:
			self.registar_historico(
				{
					"acao": "Saldo insuficiente na Conta Especial",
					"valor": valor
				}
			)

			return False
		

#cadastrar contas
def cadastrarConta():
	limpar_tela()
	print "CADASTRAR CONTA: CLIENTE"
	print "----------------------------------"

	nome = raw_input("Nome: ")
	telefone = raw_input("Telefone: ")

	cliente = Cliente(nome, telefone)

	print "\nCADASTRAR CONTA: CONTA"
	print "----------------------------------"

	numero = raw_input("Numero: ")
	saldo = float(raw_input("Saldo: "))	
	print "\nCADASTRAR CONTA: CONTA ESPECIAL ?"
	print "----------------------------------"

	especial = raw_input("Especial (S/N): ")
	 
	if especial.upper() == 'S':
		limite = float(raw_input("Limite: "))
		conta = ContaEspecial(cliente, numero, saldo, limite)
	else:
		conta = Conta(cliente, numero, saldo)

	contas.append(conta)

#Consultar Saldo
def extratoConta():
	limpar_tela()

	print "BANCO PYTHON - EXTRATO"
	print "----------------------------------"

	conta_numero = int(raw_input("\nNúmero da Conta: "))

	for conta in contas:
		if int(conta.numero) == conta_numero:
			# Imprime Cliente
			conta.imprimir_cliente();
			conta.imprimir_conta();
			conta.imprimir_historico();

			raw_input()

#Sacar valor da Conta
def sacarValor():
	limpar_tela()

	print "BANCO PYTHON - SACAR"
	print "----------------------------------"

	conta_numero = int(raw_input("\nNúmero da Conta: "))
	valor = float(raw_input("\nValor: "))

	for conta in contas:
		if int(conta.numero) == conta_numero:
			if conta.especial:
				saque = conta.saqueEspecial(valor)
			else:
				saque = conta.sacar(valor);
			
			if saque == True:
				raw_input("\nOperacao efetuada com sucesso")
			else:
				raw_input("\nSaldo insuficiente para a operação")

#Depositar valor da Conta
def depositarValor():
	limpar_tela()

	print "BANCO PYTHON - DEPOSITO"
	print "----------------------------------"

	conta_numero = int(raw_input("\nNúmero da Conta: "))
	valor = float(raw_input("\nValor: "))

	for conta in contas:
		if int(conta.numero) == conta_numero:
			conta.depositar(valor);
			raw_input("\nOperacao efetuada com sucesso")


#limpar tela
def limpar_tela():
	try:
		os.system('clear')
	except:
		os.system('cls')

#menu principal
def menu():
	limpar_tela()

	opcoes = ["Cadastrar Contas", "Saque", "Deposito", "Extrato", "Sair"]
	acao = 0

	while True:
		limpar_tela()
		print "BANCO PYTHON - MENU PRINCIPAL"
		print "----------------------------------"
		
		for index, value in enumerate(opcoes):
			print "{0}) {1}".format((index + 1), value)

		acao = int(raw_input("\nEscolha uma das opcoes: "))

		if acao == 1:
			cadastrarConta()
		elif acao == 2:
			sacarValor()
		elif acao == 3:
			depositarValor()
		elif acao == 4:
			extratoConta()
		elif acao == 5:
			exit()

#inicializar o app
menu()