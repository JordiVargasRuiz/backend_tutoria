from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Obtener la API Key
api_key = os.getenv("API_KEY")

if not api_key:
    print("⚠️ No se encontró API_KEY en las variables de entorno. Verifica la configuración en Render.")
else:
    print("✅ API Key cargada correctamente.")

# Configurar Google Generative AI
try:
    genai.configure(api_key=api_key)
    print("✅ API Key configurada en genai.")
except Exception as e:
    print(f"❌ Error al configurar genai: {str(e)}")

# Inicializar Flask
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])  # ✅ Ruta raíz para evitar error 404
def home():
    return jsonify({"mensaje": "Bienvenido a la API"}), 200

@app.route("/preguntar", methods=["POST"])
def preguntar():
    try:
        data = request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "No se recibió una pregunta"}), 400

        # Verificar si genai está configurado correctamente
        if not api_key:
            return jsonify({"error": "API Key no configurada correctamente"}), 500

        modelo = genai.GenerativeModel("gemini-1.5-pro-latest")
        respuesta = modelo.generate_content(pregunta)

        return jsonify({"respuesta": respuesta.text})

    except Exception as e:
        print(f"❌ Error en /preguntar: {str(e)}")  # Log del error en Render
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Servidor corriendo en http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)

