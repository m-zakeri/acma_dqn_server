from application import app, api
from flask import jsonify
from flask_restplus import Resource, fields
from application.dqn import DQN
from werkzeug.exceptions import BadRequest


# Swagger models:

get_q_values_request_body_model = api.model('DQNInput', {
    'state': fields.List(fields.Float)
})

train_model_request_body_model = api.model('DQNTrainModel', {
    'state': fields.List(fields.Float),
    'q_values': fields.List(fields.Float)
})


# error handling functions:
def evaluate_state(state):
    if len(state) != DQN.get_state_regular_len():
        raise BadRequest("Size of 'state' tensor must be {0} but length of the state you sent is {1}!"
                         .format(DQN.get_state_regular_len(), len(state)))

    if not all(isinstance(e, float) or isinstance(e, int) for e in state):
        raise BadRequest("Every element of 'state' must be integer or float")


def evaluate_q_values(q_values):
    if len(q_values) != DQN.get_q_values_list_regular_len():
        raise BadRequest("Size of 'q_values' tensor must be {0} but length of the q_values you sent is {1}!"
                         .format(DQN.get_q_values_list_regular_len(), len(q_values)))

    if not all(isinstance(e, float) or isinstance(e, int) for e in q_values):
        raise BadRequest("Every element of 'q_values' must be integer or float")


# APIs:

@api.route('/get-q-values/')
class GetQValues(Resource):
    @api.doc(body=get_q_values_request_body_model)
    def post(self):
        data = api.payload
        state = data['state']
        evaluate_state(state)
        dic = {
            'q_values': DQN.get_q_values(state=state)
        }
        return jsonify(dic)


@api.route('/train/')
class TrainModel(Resource):
    @api.doc(body=train_model_request_body_model)
    def post(self):
        data = api.payload
        state = data['state']
        q_values = data['q_values']
        evaluate_state(state)
        evaluate_q_values(q_values)
        DQN.train(state=state, q_values=q_values)
        return jsonify({'message': 'q_values updated successfully.'})









