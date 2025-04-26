from flask import Flask, render_template,redirect,url_for,jsonify
from flask import request
import os
from werkzeug.utils import secure_filename
from models import File, create_file,delete_file
from datetime import date
from tables import create_graph

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre-nosotros")
def about():
    return render_template("about.html")

@app.route("/documentacion")
def docs():
    return render_template("docs.html")

@app.route("/contacto")
def contact():
    return render_template("contact.html")

@app.route("/privacidad")
def privacy():
    return render_template("privacy.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/uploads", methods=['POST'])
def uploads():
    if 'file' not in request.files:
        return "No se ha enviado ningún archivo", 400

    archivo = request.files['file']

    if archivo.filename == '':
        return "Nombre de archivo vacío", 400

    filename = secure_filename(archivo.filename)
    
    if not filename.lower().endswith('.csv'):
        return jsonify({"success": False, "message": "Solo se permiten archivos CSV."}), 400
    
    try:
        import pandas as pd
        df = pd.read_csv(archivo)
        archivo.seek(0)  
    except Exception as e:
        return jsonify({"success": False, "message": "El archivo no tiene formato CSV válido."}), 400
    
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Crear carpeta si no existe
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        archivo.save(save_path)
        
        print(f"Archivo guardado en: {save_path}")

        bd = File(date.today(),archivo.filename)
        create_file(bd)
        return jsonify({"success": True, "fileName": filename}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno: {str(e)}"}), 500

   


@app.route("/graph/<filename>", methods=['GET'])
def show_graph(filename):    
    incomes_html,expenses_html,comparison_html = create_graph(filename)
    if not all([incomes_html, expenses_html, comparison_html]):
        return render_template("error.html", error_message="El archivo subido no cumple el formato esperado.")
    return render_template("graph.html",incomes=incomes_html,expenses=expenses_html,comparison=comparison_html,filename=filename)

@app.route("/delete", methods=['POST'])
def delete():

    file_name = request.form.get('fileName')

    if not file_name:
        return "No se ha enviado el nombre del archivo", 400

    path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    if os.path.exists(path):
        os.remove(path)
        print(f"Archivo eliminado correctamente.")
    else:
        print(f"El archivo no existe: {path}")

    delete_file(file_name)
    #Return de volver al inicio
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)