def create_response(data, status_code=200):
    return {"data": data, "status": "success"}, status_code

def create_error_response(message, status_code=400):
    return {"message": message, "status": "error"}, status_code
