## Lib for the wikipedia bypass
## To be used with the main client

def wiki(topic, lines = 10):
    url = "https://menu.thatrandompi.xyz/wikipedia_bypass"
    lines = str(lines) # because
    import requests as r

    re = r.get(url, headers={"topic":topic, "lines":lines})
    return re.text