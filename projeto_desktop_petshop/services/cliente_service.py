
from database import conectar
from models.cliente import Cliente


class ClienteService:

    def cadastrar_cliente(self, nome):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO clientes (nome) VALUES (?)",
            (nome,)
        )

        cliente_id = cursor.lastrowid

        conexao.commit()
        conexao.close()

        cliente = Cliente(nome)
        cliente.id = cliente_id

        return cliente

    def listar_clientes(self):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id, nome FROM clientes ORDER BY id"
        )

        resultados = cursor.fetchall()

        conexao.close()

        clientes = []

        for cliente_id, nome in resultados:
            cliente = Cliente(nome)
            cliente.id = cliente_id
            clientes.append(cliente)

        return clientes
