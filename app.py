from flask import Flask, request, jsonify
import sympy


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'name': 'math',
                    'email': 'math@outlook.com'})


@app.route('/factor', methods=['POST'])
def factor():
    request_data = request.get_json()
    student_answer = None

    if request_data:
        if 'student_response' in request_data:
            student_response = request_data['student_response']
            student_answer = sympy.factor(student_response)
            print(student_answer)

    return jsonify({'result': '{}'.format(student_answer)})


@app.route('/compare', methods=['POST'])
def compare():
    request_data = request.get_json()

    student_answer = None
    valid_answer = None

    if request_data:
        if 'valid_response' in request_data:
            student_answer = sympy.simplify(request_data['valid_response'])

        if 'student_response' in request_data:
            valid_answer = sympy.simplify(request_data['student_response'])

    return jsonify({'result': '{}'.format(student_answer == valid_answer)})


if __name__ == '__main__':
    app.run(debug=True)
