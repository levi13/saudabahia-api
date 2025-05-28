import os
from flask import Flask, request, jsonify
import google.generativeai as genai

# Configure com chave vinda da variável de ambiente
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

app = Flask(__name__)

@app.route('/')
def home():
    return "API da IA está no ar!"

@app.route('/sugestoes-refeicoes', methods=['POST'])
def sugestoes_refeicoes():
    dados = request.json
    imc = dados.get('imc')

    if imc is None:
        return jsonify({'erro': 'IMC não fornecido'}), 400

    prompt = f"Com base em um IMC de {imc}, sugira 3 refeições saudáveis para o dia."

    try:
        # Usar corretamente a criação do modelo
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

        chat = model.start_chat()
        response = chat.send_message(prompt)

        if hasattr(response, "text"):
            sugestoes = response.text.strip().split("\n")
            sugestoes = [s.strip("-• ") for s in sugestoes if s.strip()]
            return jsonify({'sugestoes': sugestoes})
        else:
            return jsonify({'erro': 'Resposta inesperada da IA'}), 500

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
