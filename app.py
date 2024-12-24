from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Sesuaikan dengan password PHPMyAdmin Anda
app.config['MYSQL_DB'] = 'cinema_db'

mysql = MySQL(app)

# Route: Tampilkan Semua Pemesanan
@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    return render_template('index.html', bookings=bookings)

# Route: Tambah Pemesanan
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        movie = request.form['movie']
        seat = request.form['seat']
        showtime = request.form['showtime']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO bookings (name, movie, seat, showtime) VALUES (%s, %s, %s, %s)",
                       (name, movie, seat, showtime))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Route: Edit Pemesanan
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        movie = request.form['movie']
        seat = request.form['seat']
        showtime = request.form['showtime']
        cursor.execute(
            "UPDATE bookings SET name=%s, movie=%s, seat=%s, showtime=%s WHERE id=%s",
            (name, movie, seat, showtime, id))
        mysql.connection.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM bookings WHERE id = %s", (id,))
    booking = cursor.fetchone()
    return render_template('edit.html', booking=booking)

# Route: Hapus Pemesanan
@app.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Menjalankan Aplikasi
if __name__ == '__main__':
    app.run(debug=True)
