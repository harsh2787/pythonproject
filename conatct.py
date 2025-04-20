from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        message = request.form['message'].strip()

        if name and email and message:
            conn = sqlite3.connect('contact.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)',
                           (name, email, message))
            conn.commit()
            conn.close()
            flash('✅ Message sent successfully!', 'success')
            return redirect('/')
        else:
            flash('⚠️ All fields are required!', 'error')

    return render_template('contact.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
