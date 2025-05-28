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

    return jsonify({'sugestoes': response.text})

if __name__ == '__main__':
    app.run(debug=True)
