import json
from lambda_authorizer import lambda_handler

# Simulate an API Gateway request with a cookie header
def test_lambda_authorizer():
    fake_event = {
        "type": "REQUEST",
        "methodArn": "arn:aws:execute-api:us-east-1:123456789012:example/prod/GET/resource",
        "headers": {
            "Cookie": "access_token=eyJraWQiOiJlTlZXRXE5SWRONE1GZUVXeFlIR09VS0FMMTVKXC83UlJydGtaOTFwSmNkRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0NGI4ZTRlOC05MDQxLTcwZmMtNGYyYS03NWY1NjhmNmVmMTYiLCJjb2duaXRvOmdyb3VwcyI6WyJiZXRhLXVzZXJzIiwidXMtZWFzdC0xX2dQdnFndFBlZ190ZXN0LXNhbWwtaWRwLW9rdGEiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZ1B2cWd0UGVnIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiMjZ0b3B2OGExYzJoZmkyMTcwcGdiNDFuODMiLCJvcmlnaW5fanRpIjoiNmE4YjdmNWYtYTMwOC00YTJiLTg3ZTUtZDJhYzk2Mzg1OGNmIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJvcGVuaWQiLCJhdXRoX3RpbWUiOjE3NTQ0NDgxNDMsImV4cCI6MTc1NDQ1MTc0MywiaWF0IjoxNzU0NDQ4MTQzLCJqdGkiOiJiYzIwMjk2YS01MjU3LTRiZDctOTI2Yy04MWYzOTg2Y2RkMzAiLCJ1c2VybmFtZSI6InRlc3Qtc2FtbC1pZHAtb2t0YV9wcmF0aWtwYmhhZ2F0QGdtYWlsLmNvbSJ9.o9e3fTKaKat_Pk3ni72l8XQnpYs_DApLSG-qKIgx1whFOCI9kzfcKzotEmjkh-CqIJz1K16xB-360CBV579M5jPbS2U1T11gc41E1oGoi6xCjOBO7B0ubRkJYbmxj3mmGH9y8NiG0urAiT0JsJG91XCZjwQLUNpSP5H-loetETJvpOnU7BOj5X0z4a1-LWduHRdBOtArDUkYqT54M-iYfP-roRF5ShefHK-38kBWnbYHTAQyK0ib5B8prmtjUVWYeoBpuYwlKIvDN1sIwEK7NVuk-ae4GXK1Bmi__chosev9-3b_EhCYwDgLTavZYgdZ-1qdyRLklXJYEVsNywzJXA"
        }
    }

    response = lambda_handler(fake_event, None)
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    test_lambda_authorizer()
