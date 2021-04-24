import requests, json

url = "https://www.lichess.org/api/games/user/macaqueattack"

r = requests.get(
    url,
    params={"max":200000, "clocks":"true", "tags":"true", "opening":"true"},
    headers={"Accept": "application/x-ndjson"}
)
r_text = r.content.decode("utf-8")
print(r_text)

games = [json.loads(s) for s in r_text.split("\n")[:-1]]


with open('games.json', 'w') as json_file:
    json.dump(games, json_file)
