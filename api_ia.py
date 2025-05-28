import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Chave da API (deixe em variável de ambiente para segurança)
genai.configure(api_key=os.environ.get("AIzaSyDSIJC26k3lH54DZCFpGYmqa6tqGShEpQo"))

@app.route('/sugestoes-refeicoes', methods=['POST'])
def sugestoes_refeicoes():
    dados = request.json
    imc = dados.get('imc')

    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Com base em um IMC de {imc}, sugira 3 refeições saudáveis para o dia."

    response = model.generate_content(prompt)

    # Supondo que response.text retorna algo assim:
    # "1. Salada de frutas\n2. Peito de frango grelhado\n3. Arroz integral"
    # Vamos transformar em lista:
    lista_sugestoes = [item.strip() for item in response.text.split('\n') if item.strip()]

    return jsonify({'sugestoes': lista_sugestoes})


if __name__ == '__main__':
    app.run(debug=True)
