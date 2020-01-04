from application import app, api
from flask import jsonify
from flask_restplus import Resource, fields
from application.dqn import DQN
from werkzeug.exceptions import BadRequest


# Swagger models:

get_q_values_request_body_model = api.model('DQNetInputModel', {
    'state': fields.List(fields.Float)
})

train_model_request_body_model = api.model('TrainModel', {
    'state': fields.List(fields.Float),
    'q_values': fields.List(fields.Float)
})

get_experience_model_request_body_model = api.model('GetExperienceModel', {
    'old_state': fields.List(fields.Float),
    'action': fields.Integer,
    'new_state': fields.List(fields.Float),
    'reward': fields.Float,
})


# error handling functions:
def get_and_evaluate_numeric_list(data, list_name, length):
    desired_list = data[list_name]
    if len(desired_list) != length:
        raise BadRequest("Size of '{0}' tensor must be {1} but length of the q_values you sent is {2}!"
                         .format(list_name, length, len(desired_list)))

    if not all(isinstance(e, float) or isinstance(e, int) for e in desired_list):
        raise BadRequest("Every element of '{}' must be integer or float.".format(list_name))

    return desired_list


def get_and_evaluate(data, element_name, element_type):
    desired_element = data[element_name]

    if not isinstance(desired_element, element_type):
        raise BadRequest("Type of the '{0}' must be {1} but it is {2}!"
                         .format(element_name, element_type.__name__, type(desired_element).__name__))

    return desired_element


def get_and_evaluate_reward(data):
    desired_element = data['reward']

    if not (isinstance(desired_element, int) or isinstance(desired_element, float)):
        raise BadRequest("Reward must be numeric but it is {}!".format(type(desired_element).__name__))

    return desired_element

# APIs:


@api.route('/get_q_values/')
class GetQValues(Resource):
    @api.doc(body=get_q_values_request_body_model)
    def post(self):
        data = api.payload
        state = get_and_evaluate_numeric_list(data, list_name='state', length=DQN.get_state_regular_len())
        dic = {
            'q_values': DQN.get_q_values(state=state)
        }
        return jsonify(dic)


@api.route('/train/')
class TrainModel(Resource):
    @api.doc(body=train_model_request_body_model)
    def post(self):
        data = api.payload
        state = get_and_evaluate_numeric_list(data, list_name='state', length=DQN.get_state_regular_len())
        q_values = get_and_evaluate_numeric_list(data, list_name='q_values', length=DQN.get_q_values_list_regular_len())
        DQN.train(state=state, q_values=q_values)
        return jsonify({'message': 'q_values updated successfully.'})


@api.route('/get_experience/')
class GetExperience(Resource):
    @api.doc(body=get_experience_model_request_body_model)
    def post(self):
        data = api.payload
        old_state = get_and_evaluate_numeric_list(data, list_name='old_state', length=DQN.get_state_regular_len())
        action = get_and_evaluate(data, element_name='action', element_type=int)
        new_state = get_and_evaluate_numeric_list(data, list_name='new_state', length=DQN.get_state_regular_len())
        reward = get_and_evaluate_reward(data)
        DQN.get_experience(old_state, action, new_state, reward)
        return jsonify({
            "message": "Now I've got more gray beard!"
        })

