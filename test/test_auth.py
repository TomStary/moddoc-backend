from moddoc.model import User


def test_login(client, db):
    # prepare data
    username = 'test'
    password = 'SuperSecret1'
    user = User(username=username, email='test@example.com', password=password)
    db.session.add(user)
    db.session.commit()

    # create data
    data = {'username': username, 'password': password}

    # get server response
    response = client.post('auth/login', json=data)

    assert response.status_code == 200
    assert response.get_json()['access_token'] is not None
