import requests

token_url = "https://id.twitch.tv/oauth2/token"
token_request = requests.post(token_url, {
    "client_id": "lfacqb746t1ldb00o1v0j6xnrf8keh",
    "client_secret": "6gcjxjdznyukse5vv3qm1a49djw24p",
    "grant_type": "client_credentials"
})
token = token_request.json()["access_token"]

url = "https://api.twitch.tv/helix/streams/?game_id=510218&language=en&first=100"
headers = {
    'client-id': 'lfacqb746t1ldb00o1v0j6xnrf8keh',
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Authorization': f"Bearer {token}"
}
r = requests.get(url, headers=headers).json()
print(r)
