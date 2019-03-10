from flask_restful import Resource, fields, marshal_with


token = {
    'token': fields.String,
}


class Login(Resource):
    @marshal_with(token)
    def post(self):
        return {'token': "yes"}
