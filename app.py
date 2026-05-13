from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__',static_folder= 'static')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@127.0.0.1/gestão_de_frotas"
db = SQLAlchemy(app)

#banco de dados dos veiculos 
class Veiculos(db.Model) : 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    placa = db.Column(db.String(10), unique = True)
    marca = db.Column(db.String(20), nullable = False)
    modelo = db.Column(db.String(50), nullable = False)
    ano_fabricacao = db.Column(db.Integer, nullable = False)
    chassi = db.Column(db.String(17), unique = True, nullable = False)
    data_aquisicao = db.Column(db.Integer, nullable=False) #quando for preencher preenche com, por exemplo, 10022000 para 10-02-2000(depois concertar para outro tipo)
    status = db.Column(db.String(20), default='Ativo')

#banco de dados de pessoas(ainda vou adicionar)


@app.route('/', methods = ["GET" , "POST"])
def loguin(): 
    return render_template('loguin.html')

@app.route ('/dashboard') 
def dashboard():
    veiculos = Veiculos.query.all()
    return render_template('dashboard.html',Veiculos = veiculos)


@app.route('/veiculos')
def veiculos(): 
    veiculos = Veiculos.query.all()
    return render_template('veiculos.html', Veiculos = veiculos)

@app.route('/veiculos/descricao/<int:id>')
def descricao_veiculo(id):
    veiculo = Veiculos.query.get_or_404(id)
    return render_template('veiculos_descricao.html', veiculo=veiculo)

@app.route('/veiculos/deletar/<int:id>')
def deletar_veiculo(id):
    veiculo = Veiculos.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('veiculos'))

@app.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    veiculo = Veiculos.query.get_or_404(id)
    
    if request.method == 'POST':
        veiculo.placa = request.form['placa']
        veiculo.marca = request.form['marca']
        veiculo.modelo = request.form['modelo']
        veiculo.ano_fabricacao = request.form['ano_fabricacao']
        veiculo.chassi = request.form['chassi']
        veiculo.data_aquisicao = request.form['data_aquisicao']
        veiculo.status = request.form['status']
        
        db.session.commit()
        return redirect(url_for('veiculos'))
    
    return render_template('veiculos_editar.html', veiculo=veiculo)


@app.route('/veiculos/cadastrar', methods=['GET', 'POST'])
def cadastro_veiculo(): 
    if request.method == 'POST':
        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano_fabricacao = request.form['ano_fabricacao']
        chassi = request.form['chassi']
        data_aquisicao = request.form['data_aquisicao']
        status = request.form['status'] 

        novo_veiculo = Veiculos(
            placa=placa,
            marca=marca,
            modelo=modelo,
            ano_fabricacao=ano_fabricacao,
            chassi=chassi,
            data_aquisicao=data_aquisicao,
            status=status
        )
        db.session.add(novo_veiculo)
        db.session.commit()
        return redirect(url_for('veiculos'))
    
    return render_template('veiculos_cadastrar.html')



with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")

if __name__ =='__main__' :
    
    app.run(debug = True)
