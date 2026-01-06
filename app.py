from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change if using another user
app.config['MYSQL_PASSWORD'] = 'janissql'  # Set your MySQL password
app.config['MYSQL_DB'] = 'voting_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

# Fetch all candidates
@app.route('/candidates', methods=['GET'])
def get_candidates():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT name FROM candidates")
        candidates = cur.fetchall()
        cur.close()
        return jsonify([{"name": row[0]} for row in candidates])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a new candidate
@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Candidate name is required"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO candidates (name, votes) VALUES (%s, 0)", (name,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": f"Candidate '{name}' added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vote for a candidate
@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    candidate = data.get('candidate')

    if not candidate:
        return jsonify({"error": "Candidate name is required"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE candidates SET votes = votes + 1 WHERE name = %s", (candidate,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": f"Vote casted for '{candidate}'!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch voting results
@app.route('/results', methods=['GET'])
def get_results():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, votes FROM candidates ORDER BY votes DESC")
        results = cur.fetchall()
        cur.close()
        return jsonify([{"name": row[0], "votes": row[1]} for row in results])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

