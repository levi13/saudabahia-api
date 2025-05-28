import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ✅ Pegar a chave de ambiente OU usar diretamente para testes
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY") or "AIzaSyDSIJC26k3lH54DZCFpGYmqa6tqGShEpQo")

@app.route('/sugestoes-refeicoes', methods=['POST'])
def sugestoes_refeicoes():
    dados = request.json
    imc = dados.get('imc')

    if imc is None:
        return jsonify({'erro': 'IMC não fornecido'}), 400

    prompt = f"Com base em um IMC de {imc}, sugira 3 refeições saudáveis para o dia."
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        sugestoes = response.text.split("\n")
        return jsonify({'sugestoes': sugestoes})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
