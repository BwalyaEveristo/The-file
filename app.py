from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root@localhost'
app.config['MYSQL_PASSWORD'] = '2003Charity@1'
app.config['MYSQL_DB'] = 'university_library'

# Initialize MySQL
mysql = MySQL(app)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Home Route for Login
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()
        if account:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect email or password', 'danger')
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(*) AS students_count FROM students')
    students_count = cursor.fetchone()['students_count']

    cursor.execute('SELECT COUNT(*) AS books_count FROM books')
    books_count = cursor.fetchone()['books_count']

    cursor.execute('SELECT COUNT(*) AS borrowed_books_count FROM borrowed_books')
    borrowed_books_count = cursor.fetchone()['borrowed_books_count']

    return render_template('dashboard.html', students_count=students_count, books_count=books_count, borrowed_books_count=borrowed_books_count)

# Student Management Route
@app.route('/student', methods=['GET', 'POST'])
def student():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['student_name']
        email = request.form['student_email']
        mobile = request.form['student_mobile']
        cursor.execute('INSERT INTO students (student_id, name, email, mobile) VALUES (%s, %s, %s, %s)', (student_id, name, email, mobile))
        mysql.connection.commit()
        flash('Student added successfully!', 'success')
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    return render_template('student.html', students=students)

# Delete Student Route
@app.route('/delete-student/<int:student_id>')
def delete_student(student_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM students WHERE student_id = %s', [student_id])
    mysql.connection.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('student'))

# Books Management Route
@app.route('/books', methods=['GET', 'POST'])
def books():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        book_id = request.form['book_id']
        book_name = request.form['book_name']
        author = request.form['book_author']
        cursor.execute('INSERT INTO books (book_id, name, author) VALUES (%s, %s, %s)', (book_id, book_name, author))
        mysql.connection.commit()
        flash('Book added successfully!', 'success')
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return render_template('books.html', books=books)

# Borrowed Books Management Route
@app.route('/borrowed-books', methods=['GET', 'POST'])
def borrowed_books():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        student_id = request.form['student_id']
        book_id = request.form['book_id']
        due_date = request.form['due_date']
        cursor.execute('INSERT INTO borrowed_books (student_id, book_id, due_date) VALUES (%s, %s, %s)', (student_id, book_id, due_date))
        mysql.connection.commit()
        flash('Book borrowed successfully!', 'success')
    cursor.execute('SELECT * FROM borrowed_books')
    borrowed_books = cursor.fetchall()
    return render_template('borrowed_books.html', borrowed_books=borrowed_books)

# Logout Route
@app.route('/logout')
def logout():
    flash('You have logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)