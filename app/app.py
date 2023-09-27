from flask import Flask, render_template,request,jsonify
from flask_mysqldb import MySQL,MySQLdb
app=Flask(__name__)


app.secret_key = "search-engine"
        
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testdata'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/search", methods=["POST", "GET"])
def search():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            search_word = request.form['query']
            filter_by = request.form['filter'] 
            sort_by = request.form['sort'] 
            print(search_word)
            if search_word == '':
                query = f"SELECT * FROM employee ORDER BY {filter_by} {sort_by}"
                cur.execute(query)
                employee = cur.fetchall()
            else:
                query = f"SELECT * FROM employee WHERE name LIKE '%{search_word}%' OR email LIKE '%{search_word}%' OR phone LIKE '%{search_word}%' ORDER BY {filter_by} {sort_by} LIMIT 20"
                cur.execute(query)
                numrows = int(cur.rowcount)
                employee = cur.fetchall()
                print(numrows)
        return jsonify({'htmlresponse': render_template('response.html', employee=employee, numrows=numrows)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()







@app.route('/details/<int:id>')
def details(id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM employee WHERE id = %s"
        cur.execute(query, (id,))
        employee = cur.fetchone()
        return render_template('details.html', employee=employee)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close() 


@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            search_word = request.form.get('query')
            if not search_word:
                return jsonify({'error': 'Search query is required'}), 400

            query = "SELECT DISTINCT name FROM employee WHERE name LIKE %s LIMIT 10"
            search_term = f"%{search_word}%"
            cur.execute(query, (search_term,))
            suggestions = cur.fetchall()
            return render_template('suggestions.html', suggestions=suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()



if __name__ == "__main__":
    app.run(debug=True)