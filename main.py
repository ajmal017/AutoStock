from Robinhood import Robinhood

device_token = "4bf09436-d26d-2869-c3f1-0e5e8c52fb40"
auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1NjcyMDk2NjcsInRva2VuIjoiYTVFRHFnQTNrSG1PVE1uSFB6c3VjblZ0QzJGMmhWIiwidXNlcl9pZCI6IjdjZjkzMDY5LTlkODUtNDFjZS1iOTVjLWIxMzU3M2E1YzdlOCIsIm9wdGlvbnMiOnRydWUsImxldmVsMl9hY2Nlc3MiOmZhbHNlfQ.IgTcLDMTvTHrYm_NTYCy2Cw1gwqS99VGcnecGGVdqkd8w_C8nR_ljkZTCzbX_azE-PJRWuSs2v4-JlsCAQCnex5L3GjmzwYXnzx5dmnW_MZFnJZn5Qg5hgu4xb_7CbmOJYcjfMflk4-Em4Q0ydoYKHOzHQdUeqspVaRFNkYmZ3GuwDMhyPFX-dLOyL_KKf7VasxAXmNJlafClss2w5X8PsHbMxb7NWnfUEQNUCc6gnjVy44BZ0T2gxEjhhfFZHbCcWyCnIWt40Km1z_JoQIu4HH8FvjJp4ESvWcAIUWUjzVYCajQfvf58_fNi9LVssqjfZ3PLCcSdkQYXqqJXFcLrQ"
refresh_token = "wCvPFp85kF62oCY8NbmILo5eXQGgwL"
USERNAME = "wdashner11@gmail.com"
PASSWORD = "erifkrad999"

robinhood = Robinhood()

robinhood.device_token = device_token
robinhood.auth_token = auth_token
robinhood.refresh_token = refresh_token
robinhood.headers['Authorization'] = 'Bearer ' + robinhood.auth_token

robinhood.user()
# except block for above line in shell.py

robinhood.login(username=USERNAME, password=PASSWORD, challenge_type="sms")

print(robinhood.quote_data("TSLA"))