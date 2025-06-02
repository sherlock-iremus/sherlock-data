import json
import requests


def get_access_token(email, password, url):
    query = f"""
mutation {{
  auth_login(email: \"{email}\", password: \"{password}\") {{
    access_token
    refresh_token
  }}
}}
"""
    r = requests.post(url + '/graphql/system', json={'query': query})
    return r.json()['data']['auth_login']['access_token']


def graphql_query(query, email, password, url):
    r = requests.post(f"{url}/graphql/?access_token={get_access_token(email, password, url)}", json={'query': query})
    return json.loads(r.text)
