from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos MySQL en Railway
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:BmnNxDfWouRvhsjwMgUaUXSllPoKuEiQ@autorack.proxy.rlwy.net:27637/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Inicialización de SQLAlchemy
db = SQLAlchemy(app)

# Modelo de datos
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

# Rutas
@app.route('/')
def index():
    """Página principal que lista todos los registros"""
    records = Record.query.all()
    return render_template('index.html', records=records)

@app.route('/record/<int:id>')
def details(id):
    """Detalles de un registro individual"""
    record = Record.query.get_or_404(id)
    return render_template('details.html', record=record)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Agregar un nuevo registro"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_record = Record(name=name, description=description)
        db.session.add(new_record)
        db.session.commit()
        flash('Record added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Editar un registro existente"""
    record = Record.query.get_or_404(id)
    if request.method == 'POST':
        record.name = request.form['name']
        record.description = request.form['description']
        db.session.commit()
        flash('Record updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', record=record)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Eliminar un registro"""
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully!')
    return redirect(url_for('index'))

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
