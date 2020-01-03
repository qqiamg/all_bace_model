# import requests
# #
# # url = 'http://192.168.99.100:8050/render.png?url=https://www.jd.com&wait=5&width=1000&height=700'
# #
# # res = requests.get(url)
# #
# # with open("1.png","wb") as f:
# #     f.write(res.content)


a = {"a": 1, "b": 123}

print(a.get("b", "1"))
