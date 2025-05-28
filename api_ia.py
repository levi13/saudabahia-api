import os
from flask import Flask, request, jsonify
import google.generativeai as genai

# Configura a API key a partir da variável de ambiente
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

app = Flask(__name__)

# Rota raiz para evitar erro 404 em GET /
@app.route('/', methods=['GET'])
def home():
    return 'API SaúdeBahia está funcionando!'

@app.route('/sugestoes-refeicoes', methods=['POST'])
def sugestoes_refeicoes():
    dados = request.json
    imc = dados.get('imc')

    if imc is None:
        return jsonify({'erro': 'IMC não fornecido'}), 400

    prompt = f"Com base em um IMC de {imc}, sugira 3 refeições saudáveis para o dia."

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            sugestoes = response.text.strip().split("\n")
            sugestoes = [s.strip("-• ") for s in sugestoes if s.strip()]
            return jsonify({'sugestoes': sugestoes})
        else:
            return jsonify({'erro': 'Sem resposta da IA'}), 500

    except Exception as e:
        print(f"[ERRO IA]: {e}")  # Útil para debugar no log do Render
        return jsonify({'erro': str(e)}), 500

# OBS: Não use app.run() em produção. O Gunicorn será usado na Render.
if __name__ == '__main__':
    app.run(debug=True)
