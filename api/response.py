from function import make_response

error_1 = "Requested object not found"
error_2 = "No valid query"
error_3 = "Incorrect query"
error_4 = "Unknown error"
error_5 = "User already exists"

response_1 = make_response(1, error_1)
response_2 = make_response(2, error_2)
response_3 = make_response(3, error_3)
response_4 = make_response(4, error_4)
response_5 = make_response(5, error_5)