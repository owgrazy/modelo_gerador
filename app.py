from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
from datetime import datetime
import os
import re

def formatar_cpf(cpf_raw):
    # Remove tudo que não for número
    numeros = re.sub(r'\D', '', cpf_raw)
    if len(numeros) == 11:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    return cpf_raw  # Se não tiver 11 dígitos, retorna do jeito que veio

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("formulario.html")

@app.route("/gerar", methods=["POST"])
def gerar():
    nome = request.form["nome"].strip().upper()
    cpf = formatar_cpf(request.form["cpf"])
    imei = request.form["imei"].strip()
    tombamento = request.form["tombamento"].strip()
    data = datetime.today().strftime("%d/%m/%Y")

    doc = DocxTemplate("modelo_termo.docx")
    contexto = {
        "nome": nome,
        "cpf": cpf,
        "imei": imei,
        "tombamento": tombamento,
        "data": data
    }
    doc.render(contexto)

    nome_arquivo = f"{nome.replace(' ', '_')}.docx"
    caminho = os.path.join("termos_gerados", nome_arquivo)

    os.makedirs("termos_gerados", exist_ok=True)
    doc.save(caminho)

    return send_file(caminho, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
