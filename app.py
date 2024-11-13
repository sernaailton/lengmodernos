#Activar el entorno virtual: source venv/bin/activate
#Desactivar el entorno virtual: deactivate

import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esta clave secreta por una más segura

# Conexión a la base de datos
def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',  # Cambia si es necesario
        password='AILTONWTF456',  # Cambia si es necesario
        db='lenguajes',  # Asegúrate que el nombre de la base de datos sea correcto
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# Ruta principal para mostrar las computadoras
@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM computadora')
        computadoras = cursor.fetchall()
    conn.close()
    return render_template('index.html', computadoras=computadoras)

# Ruta para agregar una nueva computadora
@app.route('/add_computadora', methods=['POST'])
def add_computadora():
    if request.method == 'POST':
        procesador = request.form['PROCESADOR']
        tarjeta_grafica = request.form['TARJETA_GRAFICA']
        ram = request.form['RAM']
        disco_duro = request.form['DISCO_DURO']

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO computadora (procesador, tarjeta_grafica, ram, disco_duro) VALUES (%s, %s, %s, %s)',
                (procesador, tarjeta_grafica, ram, disco_duro)
            )
            conn.commit()
        conn.close()
        flash('Computadora añadida correctamente!')
        return redirect(url_for('index'))

# Ruta para editar una computadora existente
@app.route('/edit_computadora/<int:computadora_id>', methods=['GET', 'POST'])
def edit_computadora(computadora_id):
    conn = get_db_connection()
    if request.method == 'POST':
        # Obtener los datos del formulario
        procesador = request.form['PROCESADOR']
        tarjeta_grafica = request.form['TARJETA_GRAFICA']
        ram = request.form['RAM']
        disco_duro = request.form['DISCO_DURO']

        # Actualizar la computadora en la base de datos
        with conn.cursor() as cursor:
            cursor.execute(
                'UPDATE computadora SET procesador=%s, tarjeta_grafica=%s, ram=%s, disco_duro=%s WHERE id=%s',
                (procesador, tarjeta_grafica, ram, disco_duro, computadora_id)
            )
            conn.commit()
        conn.close()
        flash('Computadora actualizada correctamente!')
        return redirect(url_for('index'))

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM computadora WHERE id = %s', (computadora_id,))
        computadora = cursor.fetchone()
    conn.close()

    return render_template('index.html', computadora=computadora)

# Ruta para eliminar una computadora
@app.route('/delete_computadora/<int:computadora_id>')
def delete_computadora(computadora_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM computadora WHERE id = %s', (computadora_id,))
        conn.commit()
    conn.close()
    flash('Computadora eliminada correctamente!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
