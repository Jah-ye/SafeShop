import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def opprett_database():
    conn = sqlite3.connect('safeshop.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bestillinger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            navn TEXT NOT NULL,
            produkt TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def er_input_sikker(tekst):
    farlige_tegn = ["<", ">", "DROP", "SELECT", "OR 1=1", ";", "--"]
    for tegn in farlige_tegn:
        if tegn in tekst.upper():
            return False
    return True

@app.route('/api/bestill', methods=['POST'])
def motta_bestilling():
    data = request.json
    navn = data.get('navn', '').strip()
    produkt = data.get('produkt', '')

    if not navn or not produkt:
        return jsonify({"status": "feil", "melding": "Du må fylle ut navnet ditt!"}), 400
        
    if not er_input_sikker(navn):
        return jsonify({"status": "feil", "melding": "Sikkerhetsfeil: Ugyldige tegn oppdaget!"}), 400

    try:
        conn = sqlite3.connect('safeshop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bestillinger (navn, produkt) VALUES (?, ?)", (navn, produkt))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok", "melding": f"Suksess! Bestillingen til {navn} er lagret i databasen."})
    except Exception as e:
        return jsonify({"status": "feil", "melding": "Det skjedde en databasefeil."}), 500

if __name__ == '__main__':
    opprett_database()
    print("Python-serveren kjører! Lytter på http://127.0.0.1:5000")
    app.run(debug=True, port=5000)