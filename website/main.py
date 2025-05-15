import sqlite3
from flask import Flask, render_template, abort

app = Flask(__name__)
DB_PATH = "database/certificates.db"

def get_certificate(cert_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, place, date, id FROM certificates WHERE id = ?", (cert_id,))
    result = cursor.fetchone()
    conn.close()
    return result

@app.route('/<cert_id>')
def verify(cert_id):
    cert = get_certificate(cert_id)
    if cert:
        name, place, date, cert_id = cert
        return render_template("index.html", name=name, place=place, date=date, cert_id=cert_id)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
