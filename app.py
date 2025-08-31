from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os


app = Flask(__name__)
app.secret_key = 'djf98ywehduysgsfg78ye8ywsd'
app.config.from_object(Config)
db = SQLAlchemy(app)

# MODELO DO PRODUTO
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    imagem = db.Column(db.String(200), nullable=True)
    categoria = db.Column(db.String(100), nullable=True)

# ROTA: HOME
@app.route("/")
def index():
    return render_template("index.html")

# ROTA: LISTAGEM DE PRODUTOS
'''@app.route("/loja")
def loja():
    produtos = Produto.query.all()
    return render_template("loja.html", produtos=produtos)
'''
@app.route("/loja")
def loja():
    categoria = request.args.get("categoria")
    if categoria:
        produtos = Produto.query.filter_by(categoria=categoria).all()
    else:
        produtos = Produto.query.all()
    return render_template("loja.html", produtos=produtos)



# ROTA: CARRINHO
@app.route("/carrinho", methods=["GET", "POST"])
def carrinho():
    if request.method == "POST":
        ids = request.form.getlist("produtos")
        selecionados = Produto.query.filter(Produto.id.in_(ids)).all()
        total = sum([p.preco for p in selecionados])
        return render_template("carrinho.html", produtos=selecionados, total=total)
    return redirect("/loja")


# ROTA: FINALIZAR VIA WHATSAPP
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

# ROTA ADMIN ESCONDIDA
@app.route("/manage-products-xyz", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        nome = request.form['nome']
        preco = float(request.form['preco'])
        descricao = request.form['descricao']
        categoria = request.form.get('categoria', '')
        
        imagem_file = request.files['imagem']
        imagem_path = ""
        if imagem_file:
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], imagem_file.filename)
            imagem_file.save(caminho)
            imagem_path = caminho

        novo = Produto(nome=nome, preco=preco, descricao=descricao, categoria=categoria, imagem=imagem_path)
        db.session.add(novo)
        db.session.commit()
        return redirect("/manage-products-xyz")

    produtos = Produto.query.all()
    return render_template("manage_xyz.html", produtos=produtos)

@app.route("/delete/<int:id>")
def delete(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect("/manage-products-xyz")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    produto = Produto.query.get_or_404(id)
    if request.method == "POST":
        produto.nome = request.form['nome']
        produto.preco = float(request.form['preco'])
        produto.descricao = request.form['descricao']
        produto.categoria = request.form.get('categoria', '')

        imagem_file = request.files['imagem']
        if imagem_file and imagem_file.filename != "":
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], imagem_file.filename)
            imagem_file.save(caminho)
            produto.imagem = caminho

        db.session.commit()
        return redirect("/manage-products-xyz")
    
    return render_template("editar_produto.html", produto=produto)


@app.route("/paginas")
def paginas():
    return render_template("paginas.html")

@app.route("/adicionar/<int:produto_id>")
def adicionar_ao_carrinho(produto_id):
    # Aqui futuramente você adiciona o produto à session['carrinho']
    print(f"Produto {produto_id} adicionado ao carrinho (simulado)")
    return redirect(url_for('loja'))




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)