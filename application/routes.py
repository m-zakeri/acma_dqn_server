from application import app, api
from flask import jsonify
from flask_restplus import Resource, fields
from application.dqn import DQ

# @app.route('/')
# def hello():
#     return 'Hello Hamid!'

person_model = api.model('Person', {
    'first-name': fields.String(required=True),
    'last-name': fields.String(required=True)
})

@api.route('/api/')
class GetAndPost(Resource):
    def get(self):
        d = {'msg': 'this is a test!'}
        return jsonify(d)

    @api.doc(body=person_model)
    def post(self):
        data = api.payload
        dic = {
            'fname': data['first-name'],
            'lname': data['last-name']
        }
        return jsonify(dic)


@api.route('/get-q-values/')
class get_q_values(Resource):
    def post(self):
        data = api.payload
        state = data['state']
        dic = {
            'q_values': DQ.network.get_q_values(state=state)
        }
        return jsonify(dic)


