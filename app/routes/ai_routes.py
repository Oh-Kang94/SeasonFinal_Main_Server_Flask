from flask_restx import Resource, fields, abort, reqparse
from flask import jsonify, request
from werkzeug.datastructures import FileStorage
from ..services.ai_service import PredictModel
from ..config.Config import api

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

def ai_routes(ai_ns):
    @ai_ns.route("/")
    class AiTest(Resource):
        @ai_ns.expect(upload_parser)
        @ai_ns.doc(
            description = '댓글 분석으로, SCORE를 측정, 긍정 부정 분류',
            responses={
            400: "Bad request. need 'review'",
            500: "Cannot find the AI Model"
        })
        def post(self):
            if 'file' not in request.files:
                abort(400, error="No file part")
            
            image_file = request.files['file']
            try:
                predictModel = PredictModel()
                result = predictModel.predictFish(image_file)
                print(result)
            except OSError:
                abort(500, error="Cannot find the AI Model")
            return result