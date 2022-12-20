from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL,MySQLdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mycondodb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
      
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route("/livesearch",methods=["POST","GET"])
def ajaxlivesearch():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            query = "SELECT * FROM condo_list"
            cur.execute(query)
            employee = cur.fetchall()
        else:    
            query = "SELECT * FROM condo_list WHERE Details LIKE '%{}%' OR Project LIKE '%{}%' OR Location LIKE '%{}%' OR Price LIKE '%{}%' ".format(search_word,search_word,search_word,search_word)
            cur.execute(query)
            numrows = int(cur.rowcount)
            employee = cur.fetchall()
            print(numrows)
    return jsonify({'htmlresponse': render_template('response.html', employee=employee, numrows=numrows)})
     
if __name__ == "__main__":
    app.run(debug=True)
    