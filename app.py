from flask import Flask, render_template, request, jsonify, send_file
import psycopg2
from psycopg2.extras import RealDictCursor
import csv
import io

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "dbname": "icecream",
    "user": "postgres",
    "password": "baze123"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


# response wrapper
def api_response(status, message, data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), status


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/datatable')
def datatable():
    return render_template('datatable.html')

def build_machines_query(search='', column='all'):
    base_query = """
        SELECT 
            m.machine_id,
            l.naziv AS lokacija,
            l.grad,
            s.naziv AS serviser,
            m.model,
            m.status,
            m.datum_posljednjeg_servisa,
            m.broj_porcioniranja_dnevno,
            m.napomena
        FROM machines m
        LEFT JOIN locations l ON m.location_id = l.location_id
        LEFT JOIN servicers s ON m.servicer_id = s.servicer_id
    """

    columns_map = {
        'lokacija': 'l.naziv',
        'grad': 'l.grad',
        'serviser': 's.naziv',
        'model': 'm.model',
        'status': 'm.status',
        'datum_posljednjeg_servisa': 'm.datum_posljednjeg_servisa',
        'broj_porcija_dnevno': 'm.broj_porcioniranja_dnevno',
        'napomena': 'm.napomena'
    }

    params = []
    if search:
        if column != 'all' and column in columns_map:
            base_query += f" WHERE {columns_map[column]}::text ILIKE %s"
            params.append(f"%{search}%")
        else:
            conditions = " OR ".join(
                [f"{col}::text ILIKE %s" for col in columns_map.values()]
            )
            base_query += f" WHERE {conditions}"
            params.extend([f"%{search}%"] * len(columns_map))

    return base_query, params

@app.route('/api/masine', methods=['GET'])
def get_masine():
    try:
        search = request.args.get('filter', '')
        column = request.args.get('column', 'all')

        conn = get_connection()
        cur = conn.cursor()
        query, params = build_machines_query(search, column)
        cur.execute(query, params)
        data = cur.fetchall()

        cur.close()
        conn.close()

        return api_response(200, "Masine dohvaćene", data)

    except Exception:
        return api_response(500, "Greška na serveru")


# GET 
@app.route('/api/masine/<int:machine_id>', methods=['GET'])
def get_masina(machine_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM machines WHERE machine_id = %s", (machine_id,))
        masina = cur.fetchone()

        cur.close()
        conn.close()

        if not masina:
            return api_response(404, "Mašina nije pronađena")

        return api_response(200, "Mašina pronađena", masina)

    except Exception:
        return api_response(500, "Greška na serveru")


# POST (create)
@app.route('/api/masine', methods=['POST'])
def create_masina():
    data = request.get_json()

    required = ['location_id', 'servicer_id', 'model', 'status']
    if not data or not all(k in data for k in required):
        return api_response(400, "Neispravni ulazni podaci")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO machines
            (location_id, servicer_id, model, status, datum_posljednjeg_servisa,
             broj_porcioniranja_dnevno, napomena)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            data['location_id'],
            data['servicer_id'],
            data['model'],
            data['status'],
            data.get('datum_posljednjeg_servisa'),
            data.get('broj_porcioniranja_dnevno'),
            data.get('napomena')
        ))

        new_machine = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return api_response(201, "Mašina dodana", new_machine)

    except Exception as e:
        return api_response(500, f"Greška na serveru: {str(e)}")



# PUT (update)
@app.route('/api/masine/<int:machine_id>', methods=['PUT'])
def update_masina(machine_id):
    data = request.get_json()
    if not data:
        return api_response(400, "Neispravni ulazni podaci")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM machines WHERE machine_id = %s", (machine_id,))
        existing = cur.fetchone()
        if not existing:
            cur.close()
            conn.close()
            return api_response(404, "Mašina nije pronađena")

        # partial update
        cur.execute("""
            UPDATE machines SET
                location_id = %s,
                servicer_id = %s,
                model = %s,
                status = %s,
                datum_posljednjeg_servisa = %s,
                broj_porcioniranja_dnevno = %s,
                napomena = %s
            WHERE machine_id = %s
            RETURNING *
        """, (
            data.get('location_id', existing['location_id']),
            data.get('servicer_id', existing['servicer_id']),
            data.get('model', existing['model']),
            data.get('status', existing['status']),
            data.get('datum_posljednjeg_servisa', existing['datum_posljednjeg_servisa']),
            data.get('broj_porcioniranja_dnevno', existing['broj_porcioniranja_dnevno']),
            data.get('napomena', existing['napomena']),
            machine_id
        ))

        updated = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return api_response(200, "Mašina ažurirana", updated)

    except Exception:
        return api_response(500, "Greška na serveru")


# DELETE
@app.route('/api/masine/<int:machine_id>', methods=['DELETE'])
def delete_masina(machine_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM machines WHERE machine_id = %s", (machine_id,))
        if not cur.fetchone():
            return api_response(404, "Mašina nije pronađena")

        cur.execute("DELETE FROM machines WHERE machine_id = %s", (machine_id,))
        conn.commit()

        cur.close()
        conn.close()

        return api_response(200, "Mašina obrisana")

    except Exception:
        return api_response(500, "Greška na serveru")


@app.route('/api/masine/grad/<string:grad>', methods=['GET'])
def masine_po_gradu(grad):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT m.* FROM machines m
            JOIN locations l ON m.location_id = l.location_id
            WHERE LOWER(l.grad) = LOWER(%s)
        """, (grad,))

        data = cur.fetchall()
        cur.close()
        conn.close()

        return api_response(200, "Mašine po gradu", data)

    except Exception:
        return api_response(500, "Greška na serveru")


@app.route('/api/masine/porcije/<int:min_porcija>', methods=['GET'])
def masine_po_porcijama(min_porcija):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM machines
            WHERE broj_porcioniranja_dnevno >= %s
        """, (min_porcija,))

        data = cur.fetchall()
        cur.close()
        conn.close()

        return api_response(200, "Mašine po broju porcija", data)

    except Exception:
        return api_response(500, "Greška na serveru")


@app.route('/api/masine/statistika', methods=['GET'])
def statistika():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) AS ukupno FROM machines")
        total = cur.fetchone()["ukupno"]

        cur.execute("""
            SELECT AVG(broj_porcioniranja_dnevno) AS prosjek,
                   MAX(broj_porcioniranja_dnevno) AS maksimum
            FROM machines
        """)
        stats = cur.fetchone()

        cur.close()
        conn.close()

        return api_response(200, "Statistika", {
            "ukupno": total,
            "prosjek_porcija": float(stats["prosjek"]) if stats["prosjek"] else 0,
            "max_porcija": stats["maksimum"]
        })

    except Exception:
        return api_response(500, "Greška na serveru")
    

@app.route('/api/download/json', methods=['GET'])
def download_json():
    try:
        search = request.args.get('filter', '')
        column = request.args.get('column', 'all')

        conn = get_connection()
        cur = conn.cursor()

        query, params = build_machines_query(search, column)
        cur.execute(query, params)
        data = cur.fetchall()

        cur.close()
        conn.close()

        return api_response(200, "JSON preuzet", data)

    except Exception:
        return api_response(500, "Greška prilikom preuzimanja JSON-a")

@app.route('/api/download/csv', methods=['GET'])
def download_csv():
    try:
        search = request.args.get('filter', '')
        column = request.args.get('column', 'all')

        conn = get_connection()
        cur = conn.cursor()

        query, params = build_machines_query(search, column)
        cur.execute(query, params)
        rows = cur.fetchall()

        if not rows:
            return api_response(404, "Nema podataka za izvoz")

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(rows[0].keys())

        for row in rows:
            writer.writerow(row.values())

        cur.close()
        conn.close()

        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='masine.csv'
        )

    except Exception:
        return api_response(500, "Greška prilikom preuzimanja CSV-a")

if __name__ == '__main__':
    app.run(debug=True)




