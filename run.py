from flask_cors import CORS
from flask import Flask, request
import json
from utility import MySqlClient

mysql_obj = MySqlClient()


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def route():
    return "To_Do App Services"


@app.route('/fetchList')
def get_to_do_list():
    try:
        select_query = "select row_to_json(t) from (select * from todo) t;"
        result = mysql_obj.execute_fetchall(select_query)
        result_data = [item for sublist in result for item in sublist]
        result_json = {'status': 'success', 'result': result_data}
        return json.dumps(result_json)
    except Exception as e:
        print("exception occurred")


@app.route('/insertItem', methods=["POST"])
def insert_item():
    try:
        data = request.get_json()
        insert_data = [data['id'], data['description'], data['timeStamp']]
        insert_query = "insert into todo values (%s, %s, %s);"
        result = mysql_obj.update_table(insert_query, insert_data)
        if result:
            result_json = {'status': 'success', 'result': 'Inserted new item successfully'}
        else:
            result_json = {'status': 'failed', 'result': 'Unable to insert item'}
        return json.dumps(result_json)
    except Exception as e:
        print("exception occurred")


@app.route('/deleteItem', methods=["POST"])
def delete_item():
    try:
        data = request.get_json()
        delete_data = [data['id']]
        delete_query = "delete from todo where id = (%s);"
        result = mysql_obj.update_table(delete_query, delete_data)
        if result:
            result_json = {'status': 'success', 'result': 'Deleted item successfully'}
        else:
            result_json = {'status': 'failed', 'result': 'Unable to delete item'}
        return json.dumps(result_json)
    except Exception as e:
        print("exception occurred")


@app.route('/deleteAll', methods=["POST"])
def delete_all():
    try:
        delete_data = []
        delete_query = "delete from todo;"
        result = mysql_obj.update_table(delete_query, delete_data)
        if result:
            result_json = {'status': 'success', 'result': 'Deleted all item successfully'}
        else:
            result_json = {'status': 'failed', 'result': 'Unable to delete items'}
        return json.dumps(result_json)
    except Exception as e:
        print("exception occurred")


if __name__ == '__main__':
    app.run(host='localhost', port=9090, debug=True, threaded=True, use_reloader=False)