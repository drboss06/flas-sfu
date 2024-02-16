from flask import Flask, render_template, jsonify, request
import dicttoxml


app = Flask(__name__)

USERS = [
{"id": 1, "name": "Ashley W. Walker", "phone": "317-769-0638", "birthday": "August 12, 1999", "email": "AshleyWWalker@dayrep.com", "username": "Joull1999"},
    {"id": 2, "name": "Martin M. Johnson", "phone": "301-962-1329", "birthday": "March 20, 1964", "email": "MartinMJohnson@teleworm.us", "username": "Youde1964"},
    {"id": 3, "name": "Justina D. Wallace", "phone": "914-819-0493", "birthday": "May 18, 1994", "email": "JustinaDWallace@rhyta.com", "username": "Donfe1994"},
    {"id": 4, "name": "Jason R. King", "phone": "608-562-1533", "birthday": "February 18, 1962", "email": "JasonRKing@dayrep.com", "username": "Ginusbact"},
    {"id": 5, "name": "Leroy T. Evans", "phone": "337-570-9574", "birthday": "January 7, 1946", "email": "LeroyTEvans@armyspy.com", "username": "Atiousaing"},
]
@app.route('/users')
def users():
    return jsonify(users=USERS)

# 2. Создание POST маршрута
@app.route('/square', methods=['POST'])
def square():
    
    number = int(request.form['number'])
    
    result = number ** 2
    
    return jsonify(data={"answer": result})

@app.route('/users-list', methods=['GET'])
def users_list():
    format_type = request.args.get('format')
    if format_type == 'json':
        return jsonify(users=USERS)
    elif format_type == 'xml':
        xml = dicttoxml.dicttoxml(USERS, custom_root='users_list', attr_type=False)
        return app.response_class(xml, mimetype='application/xml')
    else:
        return 'Invalid format type'


@app.route('/users-list2', methods=['GET'])
def users_list2():
    accept_header = request.headers.get('Accept')
    if accept_header == 'application/json':
        return jsonify(users=USERS)
    elif accept_header == 'application/xml':
        xml = dicttoxml.dicttoxml(USERS, custom_root='users_list', attr_type=False)
        return app.response_class(xml, mimetype='application/xml')
    else:
        return 'Invalid accept header', 404



@app.route('/create', methods=['POST'])
def create_user():
    data = request.json
    new_user = {
        "id": len(USERS) + 1,
        "name": data['name'],
        "phone": data['phone'],
        "birthday": data['birthday'],
        "email": data['email'],
        "username": data['username']
    }
    USERS.append(new_user)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in USERS:
        if user['id'] == user_id:
            USERS.remove(user)
            return '', 204
    return 'User not found', 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    for user in USERS:
        if user['id'] == user_id:
            data = request.json
            user['name'] = data['name']
            user['phone'] = data['phone']
            user['birthday'] = data['birthday']
            user['email'] = data['email']
            user['username'] = data['username']
            return jsonify(user), 200
    return 'User not found', 404


@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    for user in USERS:
        if user['id'] == user_id:
            data = request.json
            if 'name' in data:
                user['name'] = data['name']
            if 'phone' in data:
                user['phone'] = data['phone']
            return jsonify(user), 200
    return 'User not found', 404


if __name__ == '__main__':
    app.run()