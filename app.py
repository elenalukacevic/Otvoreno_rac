from flask import Flask, render_template, request, jsonify, send_file
import psycopg2
import csv
import io
import os
import json

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "database": "icecream",
    "user": "postgres",
    "password": "baze123"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

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

    # Mapiranje zbog join-a
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
            conditions = " OR ".join([f"{col}::text ILIKE %s" for col in columns_map.values()])
            base_query += f" WHERE {conditions}"
            params.extend([f"%{search}%"] * len(columns_map))
    
    return base_query, params



@app.route('/api/masine', methods=['GET'])
def get_masine():
    search = request.args.get('filter', '')
    column = request.args.get('column', 'all')

    conn = get_connection()
    cur = conn.cursor()

    query, params = build_machines_query(search, column)
    cur.execute(query, params)

    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    data = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()
    return jsonify({"status": "OK", "response": data})


@app.route('/api/download/json')
def download_json():
    search = request.args.get('filter', '')
    column = request.args.get('column', 'all')

    conn = get_connection()
    cur = conn.cursor()

    query, params = build_machines_query(search, column)
    cur.execute(query, params)

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    data = [dict(zip(cols, row)) for row in rows]

    cur.close()
    conn.close()
    return jsonify(data)


@app.route('/api/download/csv')
def download_csv():
    search = request.args.get('filter', '')
    column = request.args.get('column', 'all')

    conn = get_connection()
    cur = conn.cursor()

    query, params = build_machines_query(search, column)
    cur.execute(query, params)

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(cols)
    writer.writerows(rows)
    output.seek(0)

    cur.close()
    conn.close()

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="masine.csv"
    )



if __name__ == '__main__':
    app.run(debug=True)


