## Lib for the wikipedia bypass
## To be used with the main client

def wiki(topic, lines = 10):
    url = "https://testing.thatrandompi.xyz/wikipedia_bypass"
    lines = str(lines) # because
    import requests as r
    import wikipedia
    try: 
        # Try getting straight from wikipedia
        result = wikipedia.summary(topic, sentences = lines)
        return result
    except:
        try:
            # Try getting it from the bypass
            re = r.get(url, headers={"topic":topic, "lines":lines})
            obj = re.json()
            return obj["content"]
        except:
            # If all else fails...
            return dummy(topic)

def dummy(topic, lines = 10):
    # Just a dummy function #
    return '''
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna.
Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin pharetra nonummy pede. Mauris et orci.
Aenean nec lorem. In porttitor. Donec laoreet nonummy augue.
Suspendisse dui purus, scelerisque at, vulputate vitae, pretium mattis, nunc. Mauris eget neque at sem venenatis eleifend. Ut nonummy.
'''