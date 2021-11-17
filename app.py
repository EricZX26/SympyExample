from flask import Flask, jsonify
from flask_restx import Api, Resource, fields
import sympy


app = Flask(__name__)
# app.config['SERVER_NAME'] = "localhost:5000"
# print(app.config)

api = Api(app, version='1', title='Questicon Validation API',
          description='Questicon Validation API')
ns = api.namespace("sympy", description="Sympy Validaiton API")

factor_request = api.model(
    "factor_fields",
    {
        "student_response": fields.String(required=True, description="student answer")
    }
)

compare_request = api.model(
    "compare_fields",
    {
        "student_response": fields.String(required=True, description="student answer"),
        "valid_response": fields.String(required=True, description="valid answer")
    }
)

result = api.model(
    'result_model',
    {
        'result': fields.String,
    }
)


@ns.route('/factor', endpoint='factor-endpoint')
class FactorClass(Resource):
    @ns.doc(id='factor', body=factor_request)
    @ns.response(200, 'Success', result)
    def post(self):
        request_data = api.payload
        student_answer = None

        if request_data:
            if 'student_response' in request_data:
                student_response = request_data['student_response']
                student_answer = sympy.factor(student_response)
                print(student_answer)

        return jsonify({'result': '{}'.format(student_answer)})


@ns.route('/compare', endpoint='compare-endpoint')
class CompareClass(Resource):
    @ns.doc(id='compare', body=compare_request)
    @ns.response(200, 'Success', result)
    def post(self):
        request_data = api.payload
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
