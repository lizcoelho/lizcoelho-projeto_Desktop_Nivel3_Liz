
from database import conectar


class VendaService:

    def cadastrar_venda(self, cliente_id, total, itens, forma_pagamento, valor):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO vendas (cliente_id, total)
            VALUES (?, ?)
            """,
            (cliente_id, total)
        )

        venda_id = cursor.lastrowid

        for item in itens:
            cursor.execute(
                """
                INSERT INTO itens_venda
                (venda_id, descricao, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
                """,
                (
                    venda_id,
                    item.descricao,
                    item.quantidade,
                    item.preco_unitario
                )
            )

        cursor.execute(
            """
            INSERT INTO pagamentos
            (venda_id, forma_pagamento, valor)
            VALUES (?, ?, ?)
            """,
            (venda_id, forma_pagamento, valor)
        )

        conexao.commit()
        conexao.close()

        return venda_id

    def listar_vendas(self):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                vendas.id,
                clientes.nome,
                vendas.total,
                itens_venda.descricao,
                itens_venda.quantidade,
                itens_venda.preco_unitario,
                pagamentos.forma_pagamento,
                pagamentos.valor
            FROM vendas
            INNER JOIN clientes
                ON vendas.cliente_id = clientes.id
            INNER JOIN itens_venda
                ON vendas.id = itens_venda.venda_id
            INNER JOIN pagamentos
                ON vendas.id = pagamentos.venda_id
            ORDER BY vendas.id
            """
        )

        resultados = cursor.fetchall()

        conexao.close()

        return resultados
