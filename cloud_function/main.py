import function_framework

@function_framework.http
def hello_world(request):

    request_json = request.get_json(silent=True)
    return {"message": "Cloud Function is working 🚀"}
