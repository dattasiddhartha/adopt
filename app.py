#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

from scripts import contract_web3

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=['GET', 'POST'])
def home():

    conn_test = contract_web3.RopstenTest()

    address = request.form.get('address')
    expiry = request.form.get('expiry')
    strike = request.form.get('strike')
    print(address, expiry, strike)

    # initialize call option
    # e.g. '0x1719D988ab96373aeA0d033c3bef16A8E283B799'
    if request.form.get('submit') == 'CreateCall':
        calloption_initialization = contract_web3.CreateCall(compiled_contract_path = 'build/contracts/ETHOptionsFactory.json', deployed_contract_address = "0x1719D988ab96373aeA0d033c3bef16A8E283B799", expiry=int(expiry), strike=int(strike))
    if request.form.get('submit') == 'ExercisePut':
        # ExercisePut
        print()
    if request.form.get('submit') == 'ExerciseCall':
        # ExerciseCall
        print()
    if request.form.get('submit') == 'SellPut':
        # SellPut
        print()
    if request.form.get('submit') == 'SellCall':
        # SellCall
        print()
    if request.form.get('submit') == 'OptionInTheMoney':
        # OptionInTheMoney
        print()


    return render_template('pages/placeholder.home.html', conn = conn_test)


def ifNull(filter):
    if filter == None:
        return True
    if filter == "":
        return True
    else:
        return False

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
