import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 1. LØSNINGSARKITEKTUR & DATABASE ---
def opprett_database():
    # Oppretter en lokal databasefil kalt 'safeshop.db'
    conn = sqlite3.connect('safeshop.db')
    cursor = conn.cursor()
    # Lager en tabell for bestillinger hvis den ikke finnes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bestillinger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            navn TEXT NOT NULL,
            produkt TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- 2. INFORMASJONSSIKKERHET (Input-validering) ---
def er_input_sikker(tekst):
    # Enkel sårbarhetsanalyse: Sjekker etter tegn som brukes i SQL-injeksjon eller skadelige skript
    farlige_tegn = ["<", ">", "DROP", "SELECT", "OR 1=1", ";"]
    for tegn in farlige_tegn:
        if tegn in tekst.upper():
            return False
    return True

# --- 3. SYSTEMUTVIKLING (API-endepunkt) ---
@app.route('/api/bestill', methods=['POST'])
def motta_bestilling():
    data = request.json
    navn = data.get('navn', '').strip()
    produkt = data.get('produkt', '')

    # Sikkerhetssjekk før databaselagring
    if not navn or not produkt:
        return jsonify({"status": "feil", "melding": "Alle felt må fylles ut!"}), 400
        
    if not er_input_sikker(navn):
        return jsonify({"status": "feil", "melding": "Ugyldige tegn oppdaget. Sikkerhetsblokkering!"}), 400

    # Sette inn data i databasen
    try:
        conn = sqlite3.connect('safeshop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bestillinger (navn, produkt) VALUES (?, ?)", (navn, produkt))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok", "melding": f"Takk {navn}! Bestillingen på {produkt} er lagret i databasen."})
    except Exception as e:
        return jsonify({"status": "feil", "melding": "Databasefeil oppstod."}), 500

if __name__ == '__main__':
    opprett_database()
    print("Serveren kjører! Gå til http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

    def start_server():
    app.run(host='0.0.0.0', port=5000)  # Starter web-appen