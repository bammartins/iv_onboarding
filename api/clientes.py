from datetime import datetime
from flask import jsonify, make_response, abort
from shortuuid import uuid

from domain.enums.status import Status
from domain.entities.user import User
from usecases.userOnboarding import UserOnboarding
from usecases.adapters.inMemoryRepository import InMemoryUserRepository

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


id1, id2, id3, id4, id5 = str(uuid()), str(uuid()), str(uuid()), str(uuid()), str(uuid())

PEOPLE = {
    id1: {
        "id": id1,
        "Nome": "ABDELHADI",
        "Sobrenome": "AMRAOUI",
        "Data_nasc": "10-01-1990",
        "Telefone": "11987657898",
        "Email" :"frb@gmail.com",
        "timestamp": get_timestamp(),
    },
    id2: {
        "id": id2,
        "Nome": "ABDON OLIVEIRA SILVA",
        "Sobrenome": "OLIVEIRA SILVA",
        "Data_nasc": "10-01-1990",
        "Telefone": "11987657898",
        "Email" :"frb@gmail.com",
        "timestamp": get_timestamp(),
    },
    id3: {
        "id": id3,
        "Nome": "ABEGAIL VALEJO",
        "Sobrenome": "VALEJO",
        "Data_nasc": "10-01-1990",
        "Telefone": "11987657898",
        "Email" :"frb@gmail.com",
        "timestamp": get_timestamp(),
    },
    id4: {
        "id": id4,
        "Nome": "ABIZAEL",
        "Sobrenome": "CAMPOS JUNIOR",
         "Data_nasc": "10-01-1990",
        "Telefone": "11987657898",
        "Email" :"frb@gmail.com",
        "timestamp": get_timestamp(),
    },
    id5: {
        "id": id5,
        "Nome": "ABRAAO",
        "Sobrenome": "DA CRUZ PEREIRA",
        "Data_nasc": "10-01-1990",
        "Telefone": "11987657898",
        "Email" :"frb@gmail.com",
        "timestamp": get_timestamp(),
    },
}

def read_all():
    dict_clientes = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
    clientes = jsonify(dict_clientes)
    qtd = len(dict_clientes)
    content_range = "clientes 0-"+str(qtd)+"/"+str(qtd)
    # Configura headers
    clientes.headers['Access-Control-Allow-Origin'] = '*'
    clientes.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    clientes.headers['Content-Range'] = content_range
    return clientes

def read_one(id):
    if id in PEOPLE:
        person = PEOPLE.get(id)
    else:
        abort(
            404, "Pessoa com ID {id} nao encontrada".format(id=id)
        )
    return person


def create(person: User):
    repo = InMemoryUserRepository()
    name = person.get("Nome", None)
    lastName = person.get("Sobrenome", None)
    birthdate = person.get("Data_Nasc", None)
    phone = person.get("Telefone", None)
    email = person.get("Email", None)
    id=str(uuid())
    newUser = User(id, name, lastName, birthdate, phone, email, Status.CREATED.value)
    
    registerUseCase = UserOnboarding(newUser, repo)
    
    # for id in PEOPLE:
    #     if Nome == PEOPLE[id]["Nome"] and Sobrenome == PEOPLE[id]["Sobrenome"]:            
    #         # Cliente já existe
    #         abort(
    #             406,
    #             "Pessoa com nome "+Nome+" e sobrenome "+Sobrenome+" ja existe"
    #         )
    #     else:
    #         continue
    
    # Cliente nao existe, pode CRIAR:

    registerUseCase.execute(newUser)
    return make_response(
        {
            'status': 201,
            'user': newUser.to_dict()
        }
    )


def update(id, person):
    if id in PEOPLE:
        PEOPLE[id]["Nome"] = person.get("Nome")
        PEOPLE[id]["Sobrenome"] = person.get("Sobrenome")
        PEOPLE[id]["Data_nasc"] = person.get("Data_nasc")
        PEOPLE[id]["Telefone"] = person.get("Telefone")
        PEOPLE[id]["Email"] = person.get("Email")
        PEOPLE[id]["timestamp"] = get_timestamp()

        return PEOPLE[id]
    else:
        abort(
            404, "Pessoa com {id} nao encontrada".format(id=id)
        )

def delete(id):
    if id in PEOPLE:
        del PEOPLE[id]
        return make_response(
            "{id} deletado com sucesso".format(id=id), 200
        )
    else:
        abort(
            404, "Pessoa com sobrenome {Sobrenome} nao encontrada".format(id=id)
        )