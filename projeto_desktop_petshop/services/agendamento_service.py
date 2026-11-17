
from database import conectar


class AgendamentoService:

    def cadastrar_agendamento(self, cliente_id, pet_id, servico, preco, data):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO agendamentos
            (cliente_id, pet_id, servico, preco, data)
            VALUES (?, ?, ?, ?, ?)
            """,
            (cliente_id, pet_id, servico, preco, data)
        )

        agendamento_id = cursor.lastrowid

        conexao.commit()
        conexao.close()

        return agendamento_id

    def listar_agendamentos(self):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                agendamentos.id,
                clientes.nome,
                pets.nome,
                agendamentos.servico,
                agendamentos.preco,
                agendamentos.data
            FROM agendamentos
            INNER JOIN clientes
                ON agendamentos.cliente_id = clientes.id
            INNER JOIN pets
                ON agendamentos.pet_id = pets.id
            ORDER BY agendamentos.id
            """
        )

        agendamentos = cursor.fetchall()

        conexao.close()

        return agendamentos
