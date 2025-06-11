# Desafio DIO - Banco Digital
# Este código implementa um sistema bancário simples com funcionalidades de cadastro de usuários, criação de contas, depósitos, saques e extratos.

import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def executar_transacao(self, conta, transacao):
        transacao.aplicar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa(Usuario):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf

class ContaBancaria:
    def __init__(self, numero, usuario):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._usuario = usuario
        self._log = LogTransacoes()

    @classmethod
    def criar_conta(cls, usuario, numero):
        return cls(numero, usuario)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def usuario(self):
        return self._usuario

    @property
    def log(self):
        return self._log

    def sacar(self, valor):
        if valor <= 0:
            print("\n[ERRO] Valor inválido para saque.")
            return False

        if valor > self._saldo:
            print("\n[ERRO] Saldo insuficiente.")
            return False

        self._saldo -= valor
        print("\n[SUCCESSO] Saque realizado.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n[ERRO] Valor inválido para depósito.")
            return False

        self._saldo += valor
        print("\n[SUCCESSO] Depósito efetuado.")
        return True

class ContaCorrente(ContaBancaria):
    def __init__(self, numero, usuario, limite=500, max_saques=3):
        super().__init__(numero, usuario)
        self._limite = limite
        self._max_saques = max_saques

    def sacar(self, valor):
        saques_realizados = len([
            t for t in self.log.transacoes if t["tipo"] == Saque.__name__
        ])

        if valor > self._limite:
            print("\n[ERRO] Limite de saque excedido.")
            return False
        if saques_realizados >= self._max_saques:
            print("\n[ERRO] Número máximo de saques atingido.")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
Conta Nº:\t{self.numero}
Titular:\t{self.usuario.nome}
"""

class LogTransacoes:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })

class Operacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def aplicar(self, conta):
        pass

class Saque(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def aplicar(self, conta):
        if conta.sacar(self.valor):
            conta.log.adicionar(self)

class Deposito(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def aplicar(self, conta):
        if conta.depositar(self.valor):
            conta.log.adicionar(self)

def menu_principal():
    menu = """\n
========== BANCO DIGITAL ==========
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q] Sair
=> """
    return input(textwrap.dedent(menu))

def buscar_usuario(cpf, usuarios):
    return next((u for u in usuarios if u.cpf == cpf), None)

def selecionar_conta(usuario):
    if not usuario.contas:
        print("\n[INFO] Usuário não possui contas.")
        return None
    return usuario.contas[0]  # Pode ser melhorado para escolha manual

def operacao_deposito(usuarios):
    cpf = input("CPF do usuário: ")
    usuario = buscar_usuario(cpf, usuarios)

    if not usuario:
        print("\n[ERRO] Usuário não encontrado.")
        return

    valor = float(input("Valor a depositar: "))
    transacao = Deposito(valor)
    conta = selecionar_conta(usuario)
    if conta:
        usuario.executar_transacao(conta, transacao)

def operacao_saque(usuarios):
    cpf = input("CPF do usuário: ")
    usuario = buscar_usuario(cpf, usuarios)

    if not usuario:
        print("\n[ERRO] Usuário não encontrado.")
        return

    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    conta = selecionar_conta(usuario)
    if conta:
        usuario.executar_transacao(conta, transacao)

def mostrar_extrato(usuarios):
    cpf = input("CPF do usuário: ")
    usuario = buscar_usuario(cpf, usuarios)

    if not usuario:
        print("\n[ERRO] Usuário não encontrado.")
        return

    conta = selecionar_conta(usuario)
    if not conta:
        return

    print("\n========= EXTRATO =========")
    transacoes = conta.log.transacoes
    if not transacoes:
        print("Sem movimentações registradas.")
    else:
        for t in transacoes:
            print(f"{t['tipo']}: R$ {t['valor']:.2f} - {t['data']}")

    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("============================")

def novo_usuario(usuarios):
    cpf = input("CPF (apenas números): ")
    if buscar_usuario(cpf, usuarios):
        print("\n[ERRO] CPF já cadastrado.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (Rua, Nº - Bairro - Cidade/UF): ")

    usuario = Pessoa(nome, nascimento, cpf, endereco)
    usuarios.append(usuario)
    print("\n[SUCCESSO] Usuário cadastrado com sucesso!")

def nova_conta(contador, usuarios, contas):
    cpf = input("CPF do titular: ")
    usuario = buscar_usuario(cpf, usuarios)

    if not usuario:
        print("\n[ERRO] Usuário não encontrado.")
        return

    conta = ContaCorrente.criar_conta(usuario, contador)
    contas.append(conta)
    usuario.adicionar_conta(conta)

    print("\n[SUCCESSO] Conta criada.")

def listar_todas_contas(contas):
    for conta in contas:
        print("-" * 40)
        print(conta)

def main():
    usuarios = []
    contas = []

    while True:
        opcao = menu_principal()

        if opcao == "d":
            operacao_deposito(usuarios)
        elif opcao == "s":
            operacao_saque(usuarios)
        elif opcao == "e":
            mostrar_extrato(usuarios)
        elif opcao == "nu":
            novo_usuario(usuarios)
        elif opcao == "nc":
            nova_conta(len(contas) + 1, usuarios, contas)
        elif opcao == "lc":
            listar_todas_contas(contas)
        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema.")
            break
        else:
            print("\n[ERRO] Opção inválida.")

main()
