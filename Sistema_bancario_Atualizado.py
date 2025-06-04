import textwrap
import datetime

# exibir data e hora atual
print(f"Data e hora atual: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [1]\tNovo usuário
    [2]\tNova conta
    [3]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))

# --- Modificações nas Funções de Transação ---

def depositar(conta, valor):
    """Realiza um depósito na conta especificada."""
    if valor > 0:
        conta['saldo'] += valor
        conta['extrato'] += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    # A conta é modificada diretamente (dicionários são mutáveis)

def sacar(*, conta, valor, limite_valor_saque, limite_qtd_saques_diario):
    """Realiza um saque da conta especificada."""
    saldo_conta = conta['saldo']
    numero_saques_conta = conta['numero_saques']

    excedeu_saldo = valor > saldo_conta
    excedeu_limite_valor = valor > limite_valor_saque
    excedeu_limite_saques = numero_saques_conta >= limite_qtd_saques_diario

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite_valor:
        print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {limite_valor_saque:.2f}. @@@")
    elif excedeu_limite_saques:
        print(f"\n@@@ Operação falhou! Número máximo de ({limite_qtd_saques_diario}) saques diários excedido. @@@")
    elif valor > 0:
        conta['saldo'] -= valor
        conta['extrato'] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta['numero_saques'] += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

def exibir_extrato(conta):
    """Exibe o extrato da conta especificada."""
    print("\n================ EXTRATO ================")
    print(f"Agência: {conta['agencia']}\tConta: {conta['numero_conta']}")
    print(f"Titular: {conta['usuario']['nome']}")
    print("------------------------------------------")
    print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
    print(f"\nSaldo:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")

# --- Funções de Usuário e Conta ---

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuario_obj): # Modificado para receber o objeto usuario
    """Cria uma nova conta e inicializa seus atributos."""
    if usuario_obj:
        print("\n=== Conta criada com sucesso! ===")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario_obj,
            "saldo": 0.0,
            "extrato": "",
            "numero_saques": 0
        }
    # Este else não deveria ser alcançado se a lógica de chamada for correta
    print("\n@@@ Falha ao criar conta: usuário inválido. @@@")
    return None


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Saldo:\t\tR$ {conta['saldo']:.2f}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# --- Nova Função Auxiliar: Selecionar Conta ---
def selecionar_conta_usuario(usuario, todas_as_contas, agencia_padrao, lista_geral_contas_para_id):
    """
    Permite ao usuário selecionar uma de suas contas ou criar uma nova.
    Retorna a conta selecionada/criada ou None.
    """
    contas_do_usuario = [conta for conta in todas_as_contas if conta['usuario']['cpf'] == usuario['cpf']]

    if not contas_do_usuario:
        print(f"\n@@@ Usuário {usuario['nome']} não possui contas. @@@")
        criar_nova = input("Deseja criar uma nova conta para este usuário? (s/n): ").lower()
        if criar_nova == 's':
            novo_numero_conta = len(lista_geral_contas_para_id) + 1
            nova_conta = criar_conta(agencia_padrao, novo_numero_conta, usuario)
            if nova_conta:
                lista_geral_contas_para_id.append(nova_conta) # Adiciona à lista principal de contas
                return nova_conta
            else:
                return None # Falha na criação
        else:
            return None # Usuário não quis criar

    elif len(contas_do_usuario) == 1:
        print(f"\nConta {contas_do_usuario[0]['numero_conta']} selecionada automaticamente.")
        return contas_do_usuario[0]
    else:
        print("\nContas disponíveis para este usuário:")
        for i, conta_usr in enumerate(contas_do_usuario):
            print(f"[{i+1}] Ag: {conta_usr['agencia']} C/C: {conta_usr['numero_conta']} Saldo: R$ {conta_usr['saldo']:.2f}")
        
        while True:
            try:
                escolha = int(input("Digite o número da conta desejada: "))
                if 1 <= escolha <= len(contas_do_usuario):
                    return contas_do_usuario[escolha - 1]
                else:
                    print("@@@ Escolha inválida. Tente novamente. @@@")
            except ValueError:
                print("@@@ Entrada inválida. Por favor, insira um número. @@@")

def main():
    LIMITE_QTD_SAQUES_DIARIO = 3
    LIMITE_VALOR_SAQUE = 500.0
    AGENCIA = "0001"

    # saldo, limite, extrato, numero_saques -> Removidos daqui, agora são por conta
    usuarios = []
    contas = [] # Lista principal que armazena todas as contas

    while True:
        opcao = menu()

        if opcao == "d": # Depositar
            print("\n--- Depósito ---")
            cpf_usuario = input("Informe o CPF do titular da conta: ")
            usuario_selecionado = filtrar_usuario(cpf_usuario, usuarios)

            if not usuario_selecionado:
                print("\n@@@ Usuário não encontrado. Crie um usuário antes de prosseguir. @@@")
                continue

            conta_para_operacao = selecionar_conta_usuario(usuario_selecionado, contas, AGENCIA, contas)

            if conta_para_operacao:
                try:
                    valor_deposito_str = input("Informe o valor do depósito: R$ ")
                    valor_deposito = float(valor_deposito_str.replace(',', '.'))
                    depositar(conta_para_operacao, valor_deposito)
                except ValueError:
                    print("\n@@@ Valor de depósito inválido. Use números. @@@")
            else:
                print("\n@@@ Operação de depósito cancelada: nenhuma conta selecionada/criada. @@@")

        elif opcao == "s": # Sacar
            print("\n--- Saque ---")
            cpf_usuario = input("Informe o CPF do titular da conta: ")
            usuario_selecionado = filtrar_usuario(cpf_usuario, usuarios)

            if not usuario_selecionado:
                print("\n@@@ Usuário não encontrado. @@@")
                continue
            
            # Para saque, o usuário precisa ter conta. Não vamos criar na hora.
            contas_do_usuario_saque = [c for c in contas if c['usuario']['cpf'] == cpf_usuario]
            if not contas_do_usuario_saque:
                print(f"\n@@@ Usuário {usuario_selecionado['nome']} não possui contas para saque. @@@")
                continue

            conta_para_operacao = selecionar_conta_usuario(usuario_selecionado, contas, AGENCIA, contas) # Reutiliza a seleção

            if conta_para_operacao:
                try:
                    valor_saque_str = input("Informe o valor do saque: R$ ")
                    valor_saque = float(valor_saque_str.replace(',', '.'))
                    sacar(
                        conta=conta_para_operacao,
                        valor=valor_saque,
                        limite_valor_saque=LIMITE_VALOR_SAQUE,
                        limite_qtd_saques_diario=LIMITE_QTD_SAQUES_DIARIO
                    )
                except ValueError:
                    print("\n@@@ Valor de saque inválido. Use números. @@@")
            else:
                print("\n@@@ Operação de saque cancelada: nenhuma conta selecionada. @@@")


        elif opcao == "e": # Extrato
            print("\n--- Extrato ---")
            cpf_usuario = input("Informe o CPF do titular da conta: ")
            usuario_selecionado = filtrar_usuario(cpf_usuario, usuarios)

            if not usuario_selecionado:
                print("\n@@@ Usuário não encontrado. @@@")
                continue
            
            contas_do_usuario_extrato = [c for c in contas if c['usuario']['cpf'] == cpf_usuario]
            if not contas_do_usuario_extrato:
                print(f"\n@@@ Usuário {usuario_selecionado['nome']} não possui contas para exibir extrato. @@@")
                continue

            conta_para_operacao = selecionar_conta_usuario(usuario_selecionado, contas, AGENCIA, contas) # Reutiliza a seleção

            if conta_para_operacao:
                exibir_extrato(conta_para_operacao)
            else:
                print("\n@@@ Operação de extrato cancelada: nenhuma conta selecionada. @@@")


        elif opcao == "1": # Novo Usuário
            criar_usuario(usuarios)

        elif opcao == "2": # Nova Conta
            print("\n--- Nova Conta ---")
            if not usuarios:
                print("\n@@@ Nenhum usuário cadastrado. Crie um usuário primeiro! @@@")
                continue

            cpf_conta = input("Informe o CPF do usuário para vincular a nova conta: ")
            usuario_da_conta = filtrar_usuario(cpf_conta, usuarios)

            if not usuario_da_conta:
                print("\n@@@ Usuário não encontrado. Não é possível criar a conta. @@@")
                continue
            
            # Geração de número de conta simples
            numero_nova_conta = len(contas) + 1
            nova_conta_obj = criar_conta(AGENCIA, numero_nova_conta, usuario_da_conta)

            if nova_conta_obj:
                contas.append(nova_conta_obj)
            # Mensagem de sucesso/falha já está em criar_conta

        elif opcao == "3": # Listar Contas
            listar_contas(contas)

        elif opcao == "q": # Sair
            print("\n=== Obrigado por usar nosso sistema! Volte sempre! ===\n")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()