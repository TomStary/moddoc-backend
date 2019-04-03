from moddoc import app


@app.jwt.user_claims_loader
def add_claims(user):
    print(user)
    return {'roles': user['roles']}
