
# Importando as classes
from models.cliente import Cliente
from models.pet import Pet
from models.atendente import Atendente
from models.gerente import Gerente
from models.banho import Banho
from models.tosa import Tosa
from models.consulta import Consulta
from models.agendamento import Agendamento
from models.petshop import PetShop
from models.venda import Venda
from models.dinheiro import Dinheiro
from models.pix import Pix
from models.cartao import Cartao
from models.sistema_pagamento import SistemaPagamento

# Importando os serviços do banco de dados
from database import criar_tabelas
from services.cliente_service import ClienteService
from services.pet_service import PetService
from services.agendamento_service import AgendamentoService
from services.venda_service import VendaService


# Criando as tabelas do banco de dados
criar_tabelas()


# Serviços
cliente_service = ClienteService()
pet_service = PetService()
agendamento_service = AgendamentoService()
venda_service = VendaService()


# Função para carregar clientes e seus pets
def carregar_clientes():
    clientes = cliente_service.listar_clientes()

    for cliente in clientes:
        cliente.pets = pet_service.listar_pets_por_cliente(cliente.id)

    return clientes


# Carregando os dados salvos no banco
clientes = carregar_clientes()


# Listas para armazenar os dados
agendamentos = []
vendas = []


# Funcionários
funcionarios = [
    Atendente("Maria", 2000),
    Gerente("Carlos", 4000)
]


# Serviços
servicos = [
    Banho(50),
    Tosa(70),
    Consulta(120)
]


# Objetos do sistema
petshop = PetShop()
sistema = SistemaPagamento()


# Menu principal
while True:
    print("\n========== PET SHOP ==========")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Cadastrar pet")
    print("4 - Listar pets")
    print("5 - Listar funcionários")
    print("6 - Consultar serviços")
    print("7 - Realizar agendamento")
    print("8 - Realizar venda e pagamento")
    print("9 - Listar agendamentos")
    print("10 - Listar vendas")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "0":
        print("\nEncerrando o sistema...")
        break

    elif opcao == "1":
        print("\n--- CADASTRAR CLIENTE ---")

        nome = input("Digite o nome do cliente: ")

        cliente = cliente_service.cadastrar_cliente(nome)
        clientes.append(cliente)

        print("Cliente cadastrado com sucesso!")

    elif opcao == "2":
        print("\n--- LISTA DE CLIENTES ---")

        clientes = carregar_clientes()

        if len(clientes) == 0:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in clientes:
                print(f"ID: {cliente.id} - {cliente}")

    elif opcao == "3":
        print("\n--- CADASTRAR PET ---")

        clientes = carregar_clientes()

        if len(clientes) == 0:
            print("Cadastre um cliente primeiro.")
        else:
            print("\nClientes cadastrados:")

            for i, cliente in enumerate(clientes):
                print(f"{i + 1} - {cliente.nome}")

            escolha = int(input("Escolha o número do cliente: "))

            if escolha >= 1 and escolha <= len(clientes):
                cliente = clientes[escolha - 1]

                nome_pet = input("Digite o nome do pet: ")
                especie = input("Digite a espécie do pet: ")

                pet = pet_service.cadastrar_pet(
                    nome_pet,
                    especie,
                    cliente.id
                )

                cliente.adicionar_pet(pet)

                print("Pet cadastrado com sucesso!")

            else:
                print("Cliente inválido!")

    elif opcao == "4":
        print("\n--- LISTA DE PETS ---")

        clientes = carregar_clientes()

        if len(clientes) == 0:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in clientes:
                print(f"\n{cliente}")

                if len(cliente.pets) == 0:
                    print("Nenhum pet cadastrado.")
                else:
                    cliente.listar_pets()

    elif opcao == "5":
        print("\n--- LISTA DE FUNCIONÁRIOS ---")

        for funcionario in funcionarios:
            print(funcionario)

            if isinstance(funcionario, Atendente):
                funcionario.atender_cliente()
            elif isinstance(funcionario, Gerente):
                funcionario.gerenciar_petshop()

    elif opcao == "6":
        print("\n--- SERVIÇOS DISPONÍVEIS ---")

        for servico in servicos:
            print(servico)

    elif opcao == "7":
        print("\n--- REALIZAR AGENDAMENTO ---")

        clientes = carregar_clientes()

        if len(clientes) == 0:
            print("Cadastre um cliente primeiro.")
        else:
            print("\nClientes cadastrados:")

            for i, cliente in enumerate(clientes):
                print(f"{i + 1} - {cliente.nome}")

            escolha = int(input("Escolha o número do cliente: "))

            if escolha >= 1 and escolha <= len(clientes):
                cliente = clientes[escolha - 1]

                if len(cliente.pets) == 0:
                    print("Esse cliente não possui pets cadastrados.")
                else:
                    print("\nPets cadastrados:")

                    for i, pet in enumerate(cliente.pets):
                        print(f"{i + 1} - {pet}")

                    escolha_pet = int(input("Escolha o número do pet: "))

                    if escolha_pet >= 1 and escolha_pet <= len(cliente.pets):
                        pet = cliente.pets[escolha_pet - 1]

                        print("\nServiços disponíveis:")

                        for i, servico in enumerate(servicos):
                            print(f"{i + 1} - {servico}")

                        escolha_servico = int(input("Escolha o serviço: "))

                        if escolha_servico >= 1 and escolha_servico <= len(servicos):
                            servico = servicos[escolha_servico - 1]

                            data = input("Digite a data do agendamento: ")

                            agendamento = Agendamento(
                                cliente,
                                pet,
                                type(servico),
                                servico.preco,
                                data
                            )

                            agendamento_service.cadastrar_agendamento(
                                cliente.id,
                                pet.id,
                                servico.nome,
                                servico.preco,
                                data
                            )

                            agendamentos.append(agendamento)

                            atendente = funcionarios[0]

                            petshop.confirmar_agendamento(
                                agendamento,
                                atendente
                            )

                            print("Agendamento salvo no banco de dados!")

                        else:
                            print("Serviço inválido!")
                    else:
                        print("Pet inválido!")
            else:
                print("Cliente inválido!")

    elif opcao == "8":
        print("\n--- REALIZAR VENDA E PAGAMENTO ---")

        clientes = carregar_clientes()

        if len(clientes) == 0:
            print("Cadastre um cliente primeiro.")
        else:
            print("\nClientes cadastrados:")

            for i, cliente in enumerate(clientes):
                print(f"{i + 1} - {cliente.nome}")

            escolha = int(input("Escolha o número do cliente: "))

            if escolha >= 1 and escolha <= len(clientes):
                cliente = clientes[escolha - 1]

                venda = Venda(cliente)

                while True:
                    print("\nServiços disponíveis:")

                    for i, servico in enumerate(servicos):
                        print(f"{i + 1} - {servico}")

                    escolha_servico = int(input("Escolha o serviço: "))

                    if escolha_servico >= 1 and escolha_servico <= len(servicos):
                        servico = servicos[escolha_servico - 1]

                        quantidade = int(input("Digite a quantidade: "))

                        venda.adicionar_item(
                            servico.nome,
                            quantidade,
                            servico.preco
                        )

                        print("Item adicionado à venda!")

                        continuar = input("Adicionar outro serviço? (s/n): ")

                        if continuar.lower() != "s":
                            break

                    else:
                        print("Serviço inválido!")

                if len(venda.itens) > 0:
                    print("\n--- RESUMO DA VENDA ---")

                    venda.exibir_venda()

                    print("\nFormas de pagamento:")
                    print("1 - Dinheiro")
                    print("2 - Pix")
                    print("3 - Cartão")

                    pagamento_escolhido = input(
                        "Escolha a forma de pagamento: "
                    )

                    forma_pagamento = None

                    if pagamento_escolhido == "1":
                        pagamento = Dinheiro()
                        forma_pagamento = "Dinheiro"

                    elif pagamento_escolhido == "2":
                        pagamento = Pix()
                        forma_pagamento = "Pix"

                    elif pagamento_escolhido == "3":
                        pagamento = Cartao()
                        forma_pagamento = "Cartão"

                    else:
                        pagamento = None
                        print("Forma de pagamento inválida!")

                    if pagamento is not None:
                        sistema.processar_pagamento(venda, pagamento)

                        total = venda.calcular_total()

                        # Salvando a venda e o pagamento no banco
                        venda_service.cadastrar_venda(
                            cliente.id,
                            total,
                            venda.itens,
                            forma_pagamento,
                            total
                        )

                        vendas.append(venda)

                        print("Venda realizada com sucesso!")
                        print("Venda e pagamento salvos no banco de dados!")

            else:
                print("Cliente inválido!")

    elif opcao == "9":
        print("\n--- AGENDAMENTOS CADASTRADOS ---")

        agendamentos = agendamento_service.listar_agendamentos()

        if len(agendamentos) == 0:
            print("Nenhum agendamento cadastrado.")
        else:
            for agendamento in agendamentos:
                print(f"\nID: {agendamento[0]}")
                print(f"Cliente: {agendamento[1]}")
                print(f"Pet: {agendamento[2]}")
                print(f"Serviço: {agendamento[3]}")
                print(f"Preço: R$ {agendamento[4]:.2f}")
                print(f"Data: {agendamento[5]}")

    elif opcao == "10":
        print("\n--- VENDAS CADASTRADAS ---")

        vendas = venda_service.listar_vendas()

        if len(vendas) == 0:
            print("Nenhuma venda cadastrada.")
        else:
            for venda in vendas:
                print(f"\nID da venda: {venda[0]}")
                print(f"Cliente: {venda[1]}")
                print(f"Total: R$ {venda[2]:.2f}")
                print(f"Item: {venda[3]}")
                print(f"Quantidade: {venda[4]}")
                print(f"Preço unitário: R$ {venda[5]:.2f}")
                print(f"Forma de pagamento: {venda[6]}")
                print(f"Valor pago: R$ {venda[7]:.2f}")

    else:
        print("\nOpção inválida! Tente novamente.")
