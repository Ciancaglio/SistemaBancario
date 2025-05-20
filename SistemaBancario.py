# Criando o Menu do Sistemas
def menu():
    print("""
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    """)

# Definindo as Variáveis principais do Sistemas
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# aqui adiciona as funções do sistema
# loop principal
while True:
    menu()
    opcao = input("Escolha uma opção: ").lower() # usuário entra com as opções

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: ")) # usuário entra com o valor de operação
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n" # formatação dos valores e quebra de linha nostrado no extrato
        else:
            print("Valor inválido para depósito.") # caso o valor da operação for invalido avisa 

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: ")) # entra com valores de saques, e definimos as funçoes para operação prosseguir com regras

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Saldo insuficiente.")
        elif excedeu_limite:
            print("O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        else:
            print("Valor inválido para saque.")

    elif opcao == "e":
        print("\n======= EXTRATO =======")
        print(extrato if extrato else "Não foram realizadas movimentações.")
        print(f"Saldo: R$ {saldo:.2f}") 
        print("=======================\n")

    elif opcao == "q":
        print("Obrigado por usar nosso banco!")
        break

    else:
        print("Operação inválida. Selecione novamente.")
