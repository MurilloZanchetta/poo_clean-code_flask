from flask import Flask, render_template, redirect, url_for
from forms import PessoaForm
from mysql import MySQLConnection, PessoaDAO
import os
from dotenv import load_dotenv

load_dotenv()




db = MySQLConnection()
db.connect()
pessoa_dao = PessoaDAO(db.connection)

class CadastroApp:
    def __init__(self):

        self.app = Flask(__name__)
        self.__secret_key = os.environ['SECRET_KEY']
        self.configure_app()
        pessoa_dao.create_table()  # Cria as tabelas se não existirem
        self.config_routes()

    def configure_app(self):

        self.app.config['SECRET_KEY'] = self.__secret_key

    def config_routes(self):

        self.app.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.app.add_url_rule('/cadastrar', view_func=self.cadastrar, methods=['GET', 'POST'])
        self.app.add_url_rule('/deletar/<int:id>', view_func=self.deletar, methods=['GET'])

    def index(self):

        pessoas = pessoa_dao.get_all_pessoas()
        return render_template('index.html', pessoas=pessoas)

    def cadastrar(self):

        form = PessoaForm()
        if form.validate_on_submit():
            nome = form.nome.data
            idade = form.idade.data
            pessoa_dao.insert_pessoa(nome, idade)
            return redirect(url_for('index'))
        return render_template('cadastrar.html', form=form)

    def deletar(self, id):

        pessoa_dao.delete_pessoa(id)
        return redirect(url_for('index'))

    def run(self):

        self.app.run(debug=True)

if __name__ == '__main__':
    app = CadastroApp()
    app.run()
