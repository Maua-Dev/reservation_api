import pytest
from src.shared.clients.user_api_client import UserAPIClient


class TestUserAPIClient:
    
    # to test this, you must declare in your .env the user mss endpoint as USER_API_URL without 
    # any route at the end (the user api client already adds the routing)

    def test_get_user(self):

        user_client = UserAPIClient()
        user_name = user_client.get_user_name('1f25448b-3429-4c19-8287-d9e64f17bc3a')

        assert user_name == 'GUSTAVO ALVES GOMES'
        
    def test_auth_user(self):
        
        #this test will only pass if user is already created in db, as method checks for this
        
        user_client = UserAPIClient()
        # the token in the next line must be updated for testing, it is not last longing
        # it must be a valid microsoft graph authentication token (jwt format)
        
        # you can get it via azure cli via the following prompts
        # az login
        # az account get-access-token --scope https://graph.microsoft.com/.default
        user_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Ii1abjloOFZOOEZuNVMxS0gyUnBmTFZJeExIbWVmUVpoaVRGd0ZwRXJ3MVEiLCJhbGciOiJSUzI1NiIsIng1dCI6Il9qTndqZVNudlRUSzhYRWRyNVFVUGtCUkxMbyIsImtpZCI6Il9qTndqZVNudlRUSzhYRWRyNVFVUGtCUkxMbyJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9jNDllMTkzOS00YjUzLTQ3MzgtYmI2NC00MWZiMjk5MGU0MWMvIiwiaWF0IjoxNzUyMzQ4MjIxLCJuYmYiOjE3NTIzNDgyMjEsImV4cCI6MTc1MjQzNDkyMSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFVUUF1LzhaQUFBQXh4MnlPNFgySmp2S0VYMFpsbmNXS292RnI1WGxhRnlqUndCWU4wUkkzcEFLd3ZpSmdnK1ZpM09NSXQyTklseVNRVjZXQXQ0cHZWSUZzNWYzZWhDU1R3PT0iLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6Ik1pY3Jvc29mdCBBenVyZSBDTEkiLCJhcHBpZCI6IjA0YjA3Nzk1LThkZGItNDYxYS1iYmVlLTAyZjllMWJmN2I0NiIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiTFVJWiBTRUlYQVMgSU9SSU8iLCJnaXZlbl9uYW1lIjoiTEVPTkFSRE8iLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxODkuMTIwLjcyLjU4IiwibmFtZSI6IkxFT05BUkRPIExVSVogU0VJWEFTIElPUklPIiwib2lkIjoiZDM1MWE5YjEtOTM3Zi00MjNjLWE5ZDEtOTkyOWI1Nzk1YmUxIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTEyNTEwOTIzMjUtMTAwNzM4MzU3OC05Mjk3MDEwMDAtNjQ2NTYiLCJwbGF0ZiI6IjUiLCJwdWlkIjoiMTAwMzIwMDI1NzkwRTY2MyIsInJoIjoiMS5BUThBT1JtZXhGTkxPRWU3WkVIN0taRGtIQU1BQUFBQUFBQUF3QUFBQUFBQUFBQVBBR3NQQUEuIiwic2NwIjoiQXBwbGljYXRpb24uUmVhZFdyaXRlLkFsbCBBcHBSb2xlQXNzaWdubWVudC5SZWFkV3JpdGUuQWxsIEF1ZGl0TG9nLlJlYWQuQWxsIERlbGVnYXRlZFBlcm1pc3Npb25HcmFudC5SZWFkV3JpdGUuQWxsIERpcmVjdG9yeS5BY2Nlc3NBc1VzZXIuQWxsIGVtYWlsIEdyb3VwLlJlYWRXcml0ZS5BbGwgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkLkFsbCBVc2VyLlJlYWRXcml0ZS5BbGwiLCJzaWQiOiIwMDZjYWM2OS0wMzFjLWY5ZTktZTMyOC05MjlhMTJhN2E5Y2EiLCJzdWIiOiJmeG9TLVRTaGpjRHlDQmVId1N0enozQ0RmTTNJdXV3aTJYemYta1JncTFFIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IlNBIiwidGlkIjoiYzQ5ZTE5MzktNGI1My00NzM4LWJiNjQtNDFmYjI5OTBlNDFjIiwidW5pcXVlX25hbWUiOiIyMy4wMDg0Ny00QG1hdWEuYnIiLCJ1cG4iOiIyMy4wMDg0Ny00QG1hdWEuYnIiLCJ1dGkiOiJVNG5oQ0VSdGdVZU12RUlKUXRJaUFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfZnRkIjoiSnpLckRZeVpydU1FT3k0UHJRWW1MNUJ2WVNvTmp5bG5kRTFmVmZkSkJPa0JkWE56YjNWMGFDMWtjMjF6IiwieG1zX2lkcmVsIjoiMjAgMSIsInhtc19zc20iOiIxIiwieG1zX3N0Ijp7InN1YiI6ImoyeS05b0NleWdEeTJqVUI2QUZSTjluVDk0RVAxNWgtbDc1WFBaTHpjZnMifSwieG1zX3RjZHQiOjE0NDM0ODcxNTV9.ZJXmjXXXFX0PMiGexOEoJ-BiatTRaCeL0FBeoFbvUCaVDtCv2cRUE1yxO_82Rdhn3JTcjIb7uQ5GokkA19gM65D_aOKdelxJUP7ADlW-h5IInoPX_fISnZzpTF_gYWF0e4toGQP0RHCPuXOwrvPVJnMtRJvMf0rSuBgpvL2DQnLvFC5QMzlHRLkJamcCx3CzQ4hQ4SiRZU5BB1o8-TTFUK29hcLhPv-V0FsDPA2hcD8flTP70Ivvp1Ir17Q3U9Y-FS_MXmieYs21J6Sz77rNjwQJ2kVZ0XM70aMolR2g9tZ3In8ZQueLkzTTddBjPxaUda8He_cyftaoi6lK6rvpUA"
        
        user_client = UserAPIClient()
        
        user_info = user_client.authenticate_user(token=user_token)
        
        print(user_info)