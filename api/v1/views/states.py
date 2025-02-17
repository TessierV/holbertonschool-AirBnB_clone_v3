#!/usr/bin/python3
"""import for the file
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def GET_all_State():
    """all states
    """
    state_list = []
    for state in storage.all(State).values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def GET_State(state_id):
    """get a state
    """
    state = storage.get(State, state_id)
    if state is not None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=['DELETE'], strict_slashes=False)
def DELETE_State(state_id):
    """delete a state
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_State():
    """create a state
    """
    req_dict = request.get_json()
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in req_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    new_State = State(**req_dict)
    new_State.save()
    return (jsonify(new_State.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def PUT_State(state_id):
    """update a state
    """
    put_state = storage.get(State, state_id)
    req_dict = request.get_json()
    if put_state is None:
        abort(404)
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    for key, value in req_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(put_state, key, value)
    storage.save()
    return (jsonify(put_state.to_dict()), 200)
