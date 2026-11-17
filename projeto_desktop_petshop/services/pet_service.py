
from database import conectar
from models.pet import Pet


class PetService:

    def cadastrar_pet(self, nome, especie, cliente_id):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO pets (nome, especie, cliente_id)
            VALUES (?, ?, ?)
            """,
            (nome, especie, cliente_id)
        )

        pet_id = cursor.lastrowid

        conexao.commit()
        conexao.close()

        pet = Pet(nome, especie)
        pet.id = pet_id
        pet.cliente_id = cliente_id

        return pet

    def listar_pets_por_cliente(self, cliente_id):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT id, nome, especie
            FROM pets
            WHERE cliente_id = ?
            ORDER BY id
            """,
            (cliente_id,)
        )

        resultados = cursor.fetchall()

        conexao.close()

        pets = []

        for pet_id, nome, especie in resultados:
            pet = Pet(nome, especie)
            pet.id = pet_id
            pet.cliente_id = cliente_id
            pets.append(pet)

        return pets
