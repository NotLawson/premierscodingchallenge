## Lib for the wikipedia bypass
## To be used with the main client

def wiki(topic, lines = 10):
    url = "https://testing.thatrandompi.xyz/wikipedia_bypass"
    lines = str(lines) # because
    import requests as r

    re = r.get(url, headers={"topic":topic, "lines":lines})
    obj = re.json()
    return obj["content"]