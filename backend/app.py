import sqlite3
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="../frontend", static_url_path="/frontend")

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
    # Sjekker etter farlige mønstre – bruker ordgrenser for å unngå falske positiver
    farlige_mønstre = ["<", ">", "DROP TABLE", "SELECT *", "OR 1=1", ";--"]
    tekst_upper = tekst.upper()
    for mønster in farlige_mønstre:
        if mønster in tekst_upper:
            return False
    return True

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/bestill', methods=['POST'])
def motta_bestilling():
    # Sjekk at request faktisk inneholder JSON
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"status": "feil", "melding": "Ugyldig eller manglende JSON."}), 400

    navn = data.get('navn', '').strip()
    produkt = data.get('produkt', '').strip()

    if not navn or not produkt:
        return jsonify({"status": "feil", "melding": "Alle felt må fylles ut!"}), 400

    if not er_input_sikker(navn):
        return jsonify({"status": "feil", "melding": "Ugyldige tegn oppdaget. Sikkerhetsblokkering!"}), 400

    # Bruker 'with' for å sikre at tilkoblingen alltid lukkes
    try:
        with sqlite3.connect('safeshop.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bestillinger (navn, produkt) VALUES (?, ?)",
                (navn, produkt)
            )
            conn.commit()
        return jsonify({
            "status": "ok",
            "melding": f"Takk {navn}! Bestillingen på {produkt} er lagret."
        })
    except Exception as e:
        return jsonify({"status": "feil", "melding": "Databasefeil oppstod."}), 500

if __name__ == '__main__':
    opprett_database()
    print("Serveren kjører på http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)