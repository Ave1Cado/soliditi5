from flask import Flask, render_template, request, redirect, url_for, flash
from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на свой секретный ключ

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        public_key = request.form['public_key']
        password = request.form['password']
        w3.geth.personal.unlock_account(public_key, password)
        flash('Авторизация успешна', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ошибка авторизации: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    try:
        password = request.form['password']
        account = w3.geth.personal.new_account(password)
        flash(f'Ваш аккаунт: {account}', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ошибка регистрации: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
