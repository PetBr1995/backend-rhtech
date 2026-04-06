from flask import Flask, jsonify, request

app = Flask(__name__)

candidatos = [
    {
        "id": 1,
        "nome": "Peterson Brito de Albuquerque",
        "idade": 30,
        "tempo_experiencia": 5,
        "formacao": "Graduacao",
        "habilidades": ["JavaScript", "HTML", "CSS", "React", "Node.js"],
    },
    {
        "id": 2,
        "nome": "Ana Souza Lima",
        "idade": 25,
        "tempo_experiencia": 3,
        "formacao": "Graduacao",
        "habilidades": ["HTML", "CSS", "JavaScript", "Vue.js"],
    },
    {
        "id": 3,
        "nome": "Carlos Henrique Silva",
        "idade": 32,
        "tempo_experiencia": 8,
        "formacao": "Pos-graduacao",
        "habilidades": ["Java", "Spring Boot", "SQL", "Docker"],
    },
    {
        "id": 4,
        "nome": "Mariana Oliveira Santos",
        "idade": 28,
        "tempo_experiencia": 4,
        "formacao": "Graduacao",
        "habilidades": ["Python", "Django", "PostgreSQL"],
    },
    {
        "id": 5,
        "nome": "Lucas Ferreira Costa",
        "idade": 22,
        "tempo_experiencia": 1,
        "formacao": "Tecnologo",
        "habilidades": ["HTML", "CSS", "JavaScript"],
    },
    {
        "id": 6,
        "nome": "Fernanda Alves Rocha",
        "idade": 29,
        "tempo_experiencia": 6,
        "formacao": "Graduacao",
        "habilidades": ["React", "TypeScript", "Next.js", "Tailwind"],
    },
    {
        "id": 7,
        "nome": "Joao Pedro Martins",
        "idade": 35,
        "tempo_experiencia": 10,
        "formacao": "Mestrado",
        "habilidades": ["C#", ".NET", "Azure", "SQL Server"],
    },
    {
        "id": 8,
        "nome": "Camila Ribeiro Fernandes",
        "idade": 27,
        "tempo_experiencia": 5,
        "formacao": "Graduacao",
        "habilidades": ["UX/UI", "Figma", "Adobe XD"],
    }
]


def calcular_classificacao(candidato):
    pontos = 0

    # Pontos pela experiencia
    if candidato["tempo_experiencia"] >= 8:
        pontos += 40
    elif candidato["tempo_experiencia"] >= 5:
        pontos += 30
    elif candidato["tempo_experiencia"] >= 2:
        pontos += 20
    else:
        pontos += 10

    # Pontos pela formacao
    formacao = str(candidato["formacao"]).lower()
    if "mestrado" in formacao:
        pontos += 30
    elif "pos" in formacao:
        pontos += 25
    elif "graduacao" in formacao:
        pontos += 20
    elif "tecnologo" in formacao:
        pontos += 15
    else:
        pontos += 10

    # Pontos por habilidades (5 por habilidade)
    pontos += len(candidato["habilidades"]) * 5

    # Classificacao final
    if pontos >= 85:
        classificacao = "Senior"
    elif pontos >= 65:
        classificacao = "Pleno"
    else:
        classificacao = "Junior"

    return {
        "pontuacao": pontos,
        "classificacao": classificacao
    }


@app.route('/')
def home():
    return "Welcome to the Flask API!"


@app.route('/candidatos', methods=['GET'])
def get_candidatos():
    resultado = []
    for candidato in candidatos:          # laco
        avaliacao = calcular_classificacao(candidato)
        info = {                           # manipulacao de dicionario
            "id": candidato["id"],
            "nome": candidato["nome"],
            "formacao": candidato["formacao"],
            "habilidades": candidato["habilidades"],
            "total_habilidades": len(candidato["habilidades"]),  # conta habilidades
            "pontuacao": avaliacao["pontuacao"],
            "classificacao": avaliacao["classificacao"],
        }
        resultado.append(info)
    return jsonify(resultado)


@app.route('/candidatos', methods=['POST'])
def criar_candidato():
    dados = request.get_json()

    # Validacao dos campos obrigatorios
    campos_obrigatorios = ["nome", "idade", "tempo_experiencia", "formacao", "habilidades"]
    for campo in campos_obrigatorios:          # laco de validacao
        if campo not in dados:
            return jsonify({"erro": f"Campo '{campo}' e obrigatorio!"}), 400

    # Validacao do nome (apenas letras e espacos)
    nome = dados["nome"].strip()
    if nome == "":
        return jsonify({"erro": "O campo 'nome' nao pode estar vazio!"}), 400

    for caractere in nome:                      # laco para validar caractere por caractere
        if not (caractere.isalpha() or caractere.isspace()):
            return jsonify({"erro": "O campo 'nome' nao pode conter numeros nem caracteres especiais!"}), 400

    dados["nome"] = nome

    # Validacao das habilidades (minimo de 3)
    habilidades = dados["habilidades"]
    if not isinstance(habilidades, list):
        return jsonify({"erro": "O campo 'habilidades' deve ser uma lista!"}), 400

    if len(habilidades) < 3:
        return jsonify({"erro": "O candidato deve ter no minimo 3 habilidades!"}), 400

    # Gera ID automaticamente
    novo_id = 1
    for candidato in candidatos:              # laco para achar maior ID
        if candidato["id"] >= novo_id:
            novo_id = candidato["id"] + 1

    # Monta o novo candidato
    novo_candidato = {                        # criacao de dicionario
        "id": novo_id,
        "nome": dados["nome"],
        "idade": dados["idade"],
        "tempo_experiencia": dados["tempo_experiencia"],
        "formacao": dados["formacao"],
        "habilidades": dados["habilidades"],
    }

    candidatos.append(novo_candidato)
    avaliacao = calcular_classificacao(novo_candidato)

    return jsonify({
        "mensagem": "Candidato cadastrado!",
        "candidato": novo_candidato,
        "pontuacao": avaliacao["pontuacao"],
        "classificacao": avaliacao["classificacao"],
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
