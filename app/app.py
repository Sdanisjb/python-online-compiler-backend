from logging import error
from flask import Flask, jsonify
from io import StringIO
import sys
from flask.globals import request


app = Flask(__name__)


@app.route('/compile', methods=['POST'])
def test_compile():
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    response = ""
    error_message = ""
    try:
        compiled_code = compile(request.json['code'], '<string>', 'exec')
        response = eval(compiled_code)
    except SyntaxError as err:
        error_message = err.msg
    except NameError:
        error_message = "Some variable doesn't exist"
    finally:
        sys.stdout = old_stdout
        message = mystdout.getvalue()
        return jsonify({
            "result": response,
            "std_output": message,
            "error_message": error_message
        })


if __name__ == '__main__':
    app.run(debug=True)
