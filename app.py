import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import Database
import re

app = Flask(__name__)
CORS(app)

API_KEY = 'AIzaSyDKfb0y3IhQMcx7Rmsw8ICh5MucvrtIg_s'
genai.configure(api_key=API_KEY)

db = Database()

@app.route('/alunos_notas', methods=['GET'])
def listar_notas():
    try:
        notas = db.listar_notas()
        return jsonify(notas), 200
    except Exception as e:
        print(f"Erro ao listar notas: {e}")
        return jsonify({'success': False, 'message': 'Erro ao listar notas'}), 500


@app.route('/alunos_respostas', methods=['GET'])
def listar_respostas():
    try:

        id_aluno = request.args.get('id')

        if not id_aluno:
            return jsonify({'success': False, 'message': 'ID do aluno é obrigatório!'}), 400


        try:
            id_aluno = int(id_aluno)
        except ValueError:
            return jsonify({'success': False, 'message': 'ID do aluno deve ser um número inteiro válido!'}), 400

        respostas = db.listar_respostas_por_aluno(id_aluno)

        if not respostas:
            return jsonify({'success': False, 'message': 'Nenhuma resposta encontrada para este aluno.'}), 404

        return jsonify({'success': True, 'respostas': respostas}), 200

    except Exception as e:
        print(f"Erro ao listar respostas: {e}")
        return jsonify({'success': False, 'message': 'Erro ao listar respostas.'}), 500


@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    flg_tipo = data.get('flg_tipo')

    if not nome or not email or not senha or not flg_tipo:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios!'}), 400

    if flg_tipo not in ['P', 'A']:
        return jsonify({'success': False, 'message': 'Tipo inválido!'}), 400

    usuario_existente = db.buscar_usuario_por_email(email)
    if usuario_existente:
        return jsonify({'success': False, 'message': 'E-mail já cadastrado!'}), 409

    db.inserir_usuario(nome, email, senha, flg_tipo)
    return jsonify({'success': True, 'message': f'Usuário do tipo {flg_tipo} cadastrado com sucesso!'}), 201


@app.route('/perguntas', methods=['GET', 'POST'])
def perguntas():
    try:
        if request.method == 'POST':
            data = request.get_json()
            texto = data.get('texto')


            if not texto or not texto.strip():
                return jsonify({'success': False, 'message': 'Texto da pergunta é obrigatório!'}), 400


            id_pergunta = db.inserir_pergunta(texto.strip())
            return jsonify({'success': True, 'message': 'Pergunta cadastrada com sucesso!', 'id': id_pergunta}), 201

        elif request.method == 'GET':
            perguntas = db.listar_perguntas()
            return jsonify({'success': True,
                            'perguntas': [{"id": pergunta[0], "texto": pergunta[1]} for pergunta in perguntas]}), 200
    except Exception as e:
        print(f"Erro ao processar perguntas: {e}")
        return jsonify({'success': False, 'message': 'Erro ao processar a solicitação.'}), 500


@app.route('/perguntas/<int:id>', methods=['PUT'])
def atualizar_pergunta(id):
    try:
        data = request.get_json()
        texto = data.get('texto')

        if not texto or not texto.strip():
            return jsonify({'success': False, 'message': 'Texto da pergunta é obrigatório!'}), 400


        db.atualizar_pergunta(id, texto.strip())
        return jsonify({'success': True, 'message': 'Pergunta atualizada com sucesso!'}), 200
    except Exception as e:
        print(f"Erro ao atualizar pergunta: {e}")
        return jsonify({'success': False, 'message': 'Erro ao atualizar pergunta.'}), 500


@app.route('/perguntas/<int:id>', methods=['DELETE'])
def excluir_pergunta(id):
    try:
        db.excluir_pergunta(id)
        return jsonify({'success': True, 'message': 'Pergunta excluída com sucesso!'}), 200
    except Exception as e:
        print(f"Erro ao excluir pergunta: {e}")
        return jsonify({'success': False, 'message': 'Erro ao excluir pergunta.'}), 500


@app.route('/corrigir', methods=['POST'])
def corrigir():
    data = request.get_json()


    perguntas = data['perguntas']
    respostas = data['respostas']
    id_aluno = data['id_aluno']

    try:

        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
            f"Corrija as seguintes respostas do aluno com base nas perguntas: "
            + ", ".join([f"{i + 1}. {perguntas[i]}" for i in range(len(perguntas))])
            + " e respostas: "
            + ", ".join([f"{i + 1}. {respostas[i]}" for i in range(len(respostas))])
            + ". Retorne as correções explicando onde o aluno errou e inclua a nota final no formato 'Nota final: X%', "
              "onde X é a porcentagem da nota, use apenas porcentagens inteiras e não seja tão rígida na correção."
              "e caso o aluno acerte parcialmente a pergunta, divida o que seria a nota pela metade"
        )

        resposta_gpt = response.text
        print(f"Resposta da IA: {resposta_gpt}")


        nota_match = re.search(r'Nota final:\s*(\d{1,3}\.\d+|\d{1,3})%', resposta_gpt)
        if nota_match:
            nota = float(nota_match.group(1))


            for pergunta, resposta in zip(perguntas, respostas):
                pergunta_id = db.cursor.execute(
                    "SELECT id FROM pergunta WHERE texto = ?", (pergunta,)
                ).fetchone()

                if pergunta_id:
                    db.inserir_resposta(pergunta_id[0], id_aluno, resposta)
                else:
                    print(f"Pergunta não encontrada no banco: {pergunta}")


            db.inserir_nota_aluno(id_aluno, nota, resposta_gpt)

            return jsonify({'nota': float(nota), 'respostas_corrigidas': resposta_gpt}), 200
        else:

            return jsonify({'error': 'Não foi possível extrair a nota da resposta da IA.'}), 400
    except Exception as e:
        print(f"Erro na correção: {e}")
        return jsonify({'error': 'Erro ao processar a correção.'}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('login')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'success': False, 'message': 'Campos de login e senha são obrigatórios!'}), 400

    usuario = db.buscar_usuario_por_login(email, senha)
    if usuario:
        flg_tipo = usuario[4]
        if flg_tipo == 'P':
            return jsonify({'success': True, 'message': 'Login de professor bem-sucedido!', 'tipo': 'P'})
        elif flg_tipo == 'A':
            return jsonify({'success': True, 'message': 'Login de aluno bem-sucedido!', 'tipo': 'A', 'id': usuario[0]})
    return jsonify({'success': False, 'message': 'Credenciais inválidas!'}), 401


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
