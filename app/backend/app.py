"""
app.py

This Flask application provides an inventory management system with user authentication via LDAP 
and JWT for secure API access. The application supports CRUD operations on inventory data stored 
in a PostgreSQL database. CORS is enabled to allow cross-origin requests.

Dependencies:
- Flask: Web framework for Python.
- Flask-CORS: Handling Cross-Origin Resource Sharing (CORS).
- Flask-JWT-Extended: Handling JWT authentication.
- psycopg2: PostgreSQL database adapter for Python.
- ldap: LDAP library for Python.

Configuration:
- JWT_SECRET_KEY: Secret key for JWT.
- JWT_ACCESS_TOKEN_EXPIRES: JWT expiration time.
- LDAP_HOST: Host URL for the LDAP server.
- LDAP_BASE_DN: Base DN for LDAP directory.

Routes:
- /login: Authenticate user and issue JWT.
- /inventory: Manage inventory items (GET, POST).
- /inventory/<int:id>: Manage individual inventory item (GET, DELETE).
- /inventory/delete/<int:id>: Delete an inventory item (DELETE).
- /inventory/modify/<int:id>: Modify an inventory item (PATCH).
"""
import os
import psycopg2
from flask import Flask, jsonify, request, g
from flask_cors import CORS
import ldap
from ldap import initialize, LDAPError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
CORS(app, resources={
    r"/*": {"origins": "*"},
    r"/login": {"origins": "*"},
    r"/inventory": {"origins": "*"},
    r"/inventory/*": {"origins": "*"}
})

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a strong key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)
jwt = JWTManager(app)

# LDAP Configuration
LDAP_HOST = 'ldap://ldap:1389'  # Enter your LDAP server host here
LDAP_BASE_DN = 'dc=test,dc=ch'  # Enter your LDAP directory base DN here

def get_ldap_connection():
    conn = ldap.initialize(LDAP_HOST)
    return conn

def ldap_login(username, password):
    try:
        ldap_conn = get_ldap_connection()
        ldap_conn.simple_bind_s(f"uid={username},{LDAP_BASE_DN}", password)
        return True
    except LDAPError as e:
        print(f"LDAP authentication failed: {e}")
        return False

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )
    return conn

@app.before_request
def before_request():
    g.db_conn = get_db_connection()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db_conn'):
        g.db_conn.close()

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request accepted'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response, 200

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if ldap_login(username, password):
        # Generate a new token
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/inventory', methods=['GET', 'POST', 'OPTIONS'])
@jwt_required()
def manage_inventory():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request accepted'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
        return response, 200

    if request.method == 'POST':
        try:
            data = request.get_json()
            cur = g.db_conn.cursor()
            cur.execute("""
                INSERT INTO inventory (servername, ip, netmask, netzzone, environment, os, kernel_version,
                                       application_id, av, bv, virtualisierung, hardware, firmware, cpu,
                                       memory, cmdb_status, uptime, lastupdate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                data['servername'], data['ip'], data['netmask'], data['netzzone'], data['environment'],
                data['os'], data['kernel_version'], data['application_id'], data['av'], data['bv'],
                data['virtualisierung'], data['hardware'], data['firmware'], data['cpu'], data['memory'],
                data['cmdb_status'], data['uptime'], data['lastupdate']
            ))
            new_inventory_id = cur.fetchone()[0]
            g.db_conn.commit()
            cur.close()
            return jsonify({'message': 'Inventory added successfully', 'id': new_inventory_id}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'GET':
        try:
            current_user = get_jwt_identity()
            cur = g.db_conn.cursor()
            cur.execute('SELECT id, servername, os, environment, application_id FROM inventory;')
            rows = cur.fetchall()

            colnames = [desc[0] for desc in cur.description]
            cur.close()

            items = []
            for row in rows:
                item = {}
                for i, colname in enumerate(colnames):
                    item[colname] = row[i]
                items.append(item)

            return jsonify(items)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/inventory/<int:id>', methods=['GET', 'DELETE', 'OPTIONS'])
@jwt_required()
def manage_inventory_entry(id):
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request accepted'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, DELETE')
        return response, 200

    if request.method == 'DELETE':
        try:
            cur = g.db_conn.cursor()
            cur.execute('DELETE FROM inventory WHERE id = %s RETURNING id;', (id,))
            deleted_id = cur.fetchone()[0]
            g.db_conn.commit()
            cur.close()
            return jsonify({'message': f'Inventory entry {deleted_id} deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'GET':
        try:
            cur = g.db_conn.cursor()
            cur.execute('SELECT id, servername, os, environment, application_id FROM inventory WHERE id = %s;', (id,))
            row = cur.fetchone()
            cur.close()

            if row:
                item = {
                    'id': row[0],
                    'servername': row[1],
                    'os': row[2],
                    'environment': row[3],
                    'application_id': row[4]
                }
                return jsonify(item)
            else:
                return jsonify({'error': 'Server not found'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/inventory/delete/<int:id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_inventory_entry(id):
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request accepted'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        return response, 200

    if request.method == 'DELETE':
        try:
            cur = g.db_conn.cursor()
            cur.execute('DELETE FROM inventory WHERE id = %s RETURNING id;', (id,))
            deleted_id = cur.fetchone()[0]
            g.db_conn.commit()
            cur.close()
            return jsonify({'message': f'Inventory entry {deleted_id} deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/inventory/modify/<int:id>', methods=['PATCH', 'OPTIONS'])
@jwt_required()
def modify_inventory_entry(id):
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request accepted'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'PATCH')
        return response, 200

    if request.method == 'PATCH':
        try:
            data = request.get_json()
            query_parts = []
            query_values = []
            
            for key, value in data.items():
                query_parts.append(f"{key} = %s")
                query_values.append(value)

            query_values.append(id)

            query = f"UPDATE inventory SET {', '.join(query_parts)} WHERE id = %s RETURNING id;"
            
            cur = g.db_conn.cursor()
            cur.execute(query, tuple(query_values))
            updated_id = cur.fetchone()[0]
            g.db_conn.commit()
            cur.close()
            return jsonify({'message': f'Inventory entry {updated_id} updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)