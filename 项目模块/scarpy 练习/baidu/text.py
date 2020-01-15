import requests

res = requests.get('https://s.hc360.com/seller/search.html?kwd=LED%E7%81%AF&c=&F=&G=&nselect=1')
print(res.text)