import requests
from bs4 import BeautifulSoup
import http.client
import json
from googletrans import Translator

class Summarizer():
    def __init__(self):
        pass

    def Extract(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        data = ""
        for p in soup.find_all("p"):
            
            encoded_text = p.text
            decoded_text = encoded_text.encode('latin1').decode('utf-8')
            translator = Translator()

            translated_text = translator.translate(decoded_text, src='zh-cn', dest='en')

            # Print the translated text
            data += "\n" + translated_text.text

        return data

    def GenerateSummary(self,query):
        conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")
        prompt = (
            "You have a PhD in literature,. Generate a concise summary of the data given below: -\n"+query
        )

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "system_prompt": "",
            "temperature": 0.9,
            "top_k": 5,
            "top_p": 0.9,
            "max_tokens": 256,
            "web_access": False
        }
        headers = {
            'x-rapidapi-key': "613669e2a9msh8d75f52099da82ep185d8ajsn9ff63dfef31b",
            'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
            'Content-Type': "application/json"
        }

        payload_json = json.dumps(payload)

        conn.request("POST", "/conversationgpt4-2",  payload_json, headers)

        res = conn.getresponse()
        data = res.read()
        return json.loads(data)['result']



sm = Summarizer()
print(sm.GenerateSummary(sm.Extract("https://www.gov.cn/zhengce/202406/content_6958160.htm")))

# Output: -
# On June 18th, Xinhua News Agency reported that at a press conference hosted by the National Development 
# and Reform Commission, officials stated that most economic indicators had shown improvements when comparing
#  them to those of the previous month due to continuously implemented macroeconomic policies. They 
# acknowledged the complexities posed by global uncertainties while emphasizing their focus towards promoting
#  initiatives like 'double circulation', updating large scale equipment, and replacing older consumer goods 
# with newer ones. Additionally, efforts toward enhancing cleaner forms of transport via advancements in the 
# electric car sector along with anchoring constraints around energy efficiency targets received mention during 
# the briefings. These measures collectively aim to ensure sustainable economic stability amidst ongoing worldwide fluctuations.