import json
from lambda_authorizer import lambda_handler

# Simulate an API Gateway request with a cookie header
def test_lambda_authorizer():
    fake_event = {
        "type": "REQUEST",
        "methodArn": "arn:aws:execute-api:us-east-1:123456789012:example/prod/GET/resource",
        "headers": {
            "Cookie": "access_token=eyJraWQiOiJlTlZXRXE5SWRONE1GZUVXeFlIR09VS0FMMTVKXC83UlJydGtaOTFwSmNkRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0NGI4ZTRlOC05MDQxLTcwZmMtNGYyYS03NWY1NjhmNmVmMTYiLCJjb2duaXRvOmdyb3VwcyI6WyJiZXRhLXVzZXJzIiwidXMtZWFzdC0xX2dQdnFndFBlZ190ZXN0LXNhbWwtaWRwLW9rdGEiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZ1B2cWd0UGVnIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiMjZ0b3B2OGExYzJoZmkyMTcwcGdiNDFuODMiLCJvcmlnaW5fanRpIjoiNGE5ODZhM2QtNzViYy00ZmQyLTg1MDYtM2ZkN2U0Y2Q1Y2I5IiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJvcGVuaWQiLCJhdXRoX3RpbWUiOjE3NTQ0NDQ1MDksImV4cCI6MTc1NDQ0ODEwOSwiaWF0IjoxNzU0NDQ0NTEwLCJqdGkiOiIzNDAyNDVhYS1jMTQ2LTRhOTMtOWZhZS1iOTc3Y2U3YWM4YTMiLCJ1c2VybmFtZSI6InRlc3Qtc2FtbC1pZHAtb2t0YV9wcmF0aWtwYmhhZ2F0QGdtYWlsLmNvbSJ9.edcKSqZ_5alICrKkNpzrQRkqXQ-9fKP2aSVWgwQ2GN9R6jg6cF5pGWjNQ-kU7eZvO2Yeh_gb-dM8JNVs4VhrwQNoC3KI69rNXXKqaB4iC7LFQoGg98epIza3qIOAebayaIaNjoT3LixFIvvqclVYBdDobHulfj_ts0b6lMcS2fpckAN7gmjHkXtmUyivLcno1r8y_VRVjWIM-0aGNmKB3qwv-xKUmssG-6dMkuwk-v0U3anoDRGFIeyZ1_waYGFzXMG-o7aPQ-NiY5CVaN6LYYVAQ2RM0RjHb525djtkGYFTnQGwn2Qurh4gzNAvzLMFumkbr4RpJguHYKGUFfBD-Q"
        }
    }

    response = lambda_handler(fake_event, None)
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    test_lambda_authorizer()
