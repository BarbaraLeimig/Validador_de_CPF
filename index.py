#Validação de CPF
#pip install Flask
import pymysql

db = pymysql.connect(host="127.0.0.1",
                     user="root",
                     password="teste",
                     database="ValidaCPF")

from flask import Flask, render_template, request

app = Flask(__name__)

def calcula_cpf(cpf):
  # Remove caracteres não numéricos
  cpf = ''.join(filter(str.isdigit, cpf))

  # Verifica se o CPF tem 11 dígitos ou se todos são iguais
  if len(cpf) != 11 or len(set(cpf)) == 1:
      return False

  v1 = v2 = 0
  for i in range(9):
      v1 += int(cpf[8 - i]) * (9 - (i % 10))
      v2 += int(cpf[8 - i]) * (9 - ((i + 1) % 10))
      print(i, cpf[8 - i], v1, v2)

  v1 = (v1 % 11) % 10
  v2 += v1 * 9
  v2 = (v2 % 11) % 10
  
  return cpf.endswith(str(v1) + str(v2))


# Exemplo de uso

@app.route('/')
def index():
  cursor = db.cursor()
  sql = "SELECT * FROM parceiros;"
  cursor.execute(sql)
  parceiros = cursor.fetchall()
  return render_template('index.html', parceiros = parceiros)  # Nome do arquivo HTML que contém o formulário

@app.route('/validar_cpf', methods=['POST'])
def validar_cpf():
    cpf = request.form['cpf']  # 'cpf' é o nome do campo no seu formulário HTML
    if calcula_cpf(cpf):
      nome = request.form['nome']
      cursor = db.cursor()

      # Define a consulta SQL para inserir o CPF na tabela
      sql= "INSERT INTO parceiros (cpf, nome) VALUES ('"
      sql += cpf +  "','" + nome + "');"

      # executa a consulta SQL como o valor do CPF
      cursor.execute(sql)

      #Confirma a inserção dos dados no banco de dados
      db.commit()
      
      return '<p>CPF válido e processado.</p>' +\
             '<p>Para inserir um novo parceiro, clique <a href="http://127.0.0.1:5000/">aqui!</a></p>'
    else:
      return '<p style="color:red">CPF <b>inválido</b>.</p>' +\
             '<button onclick="history.back()">Voltar</button>'

if __name__ == '__main__':
  app.run(debug=True)
