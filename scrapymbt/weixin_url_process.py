# 处理微信公众号分页的url，以&为分隔号获取参数

url = "action=getmsg&__biz=MzA3NjUxNTM4Nw==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=ODc0NDUwMDAz&key=140bdc387030f4128d5156433a767b9ae2ce38d458943837da761a4cdfd8b3baf62b043496d20022b5798c54f205b95feb3d8951a77829d278166400bad6bf1cf1d46af8103c961c44aa21532d66746fb483e043c743c7c7c2364de17429d4ea3da28d2b80be3bc687943584933595e041abb2622905b6c3a24774a891457606&pass_ticket=AF%2BD1kO6wUoyHTJhNeEze%2BKMefHJqr8IrYLlu4DkuqAOKjOtgI25ikD0vak7CXYGbGwyr5jr63mhovmJv3MdWw%3D%3D&wxtoken=&appmsg_token=1210_EWNkabaUyV9%252BnoQTaDRnyVez-oKD10W1z9028g~~&x5=0&f=json"
l = url.split("&")

for i in l:
    print(i)
