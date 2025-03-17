from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

print("API Key cargada:", os.getenv("API_KEY"))


@app.route("/preguntar", methods=["POST"])
def preguntar():
    try:
        data = request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "No se recibió una pregunta"}), 400

        modelo = genai.GenerativeModel("gemini-1.5-pro-latest")
        respuesta = modelo.generate_content(pregunta)

        return jsonify({"respuesta": respuesta.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
