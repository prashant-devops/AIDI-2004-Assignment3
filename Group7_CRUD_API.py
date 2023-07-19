from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configure the PostgreSQL database connection
config = {
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres',
    # 'user': 'admin1',
    # 'password': 'admin@123'
}

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    amount_due = data.get('amount_due')

    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO students (first_name, last_name, dob, amount_due)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id
    ''', (first_name, last_name, dob, amount_due))

    student_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'student_id': student_id}), 201

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student is None:
        return jsonify({'message': 'Student not found'}), 404

    student_data = {
        'student_id': student[0],
        'first_name': student[1],
        'last_name': student[2],
        'dob': student[3],
        'amount_due': student[4]
    }

    return jsonify(student_data)

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    amount_due = data.get('amount_due')

    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE students
        SET first_name = %s, last_name = %s, dob = %s, amount_due = %s
        WHERE student_id = %s
    ''', (first_name, last_name, dob, amount_due, student_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Student updated'})

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM students WHERE student_id = %s', (student_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Student deleted'})

@app.route('/students', methods=['GET'])
def get_all_students():
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    student_data = []
    for student in students:
        student_data.append({
            'student_id': student[0],
            'first_name': student[1],
            'last_name': student[2],
            'dob': student[3],
            'amount_due': student[4]
        })

    return jsonify(student_data)

if __name__ == '__main__':
    app.run(debug=True)