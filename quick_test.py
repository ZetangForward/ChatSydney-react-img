from EdgeGPT.EdgeGPT import Chatbot
import base64  
from PIL import Image  
from io import BytesIO  
import json
import asyncio  
import traceback

context = ""

user_message = "请问这个图片上面是什么？"
bot_mode = "precise"  # creative

with open("cookies.json", 'r') as f:
    cookies = json.load(f)
SRCHHPGUSR = {
                "creative": "cdxtone=Creative&cdxtoneopts=h3imaginative,gencontentv3,nojbfedge",
                "precise": "cdxtone=Precise&cdxtoneopts=h3precise,clgalileo,gencontentv3,nojbfedge",
                "balanced": "cdxtone=Balanced&cdxtoneopts=galileo,fluxhint,glfluxv13,nojbfedge"
            }
cookies = list(filter(lambda d: d.get('name') != 'SRCHHPGUSR', cookies)) + [{"name": "SRCHHPGUSR","value": SRCHHPGUSR[bot_mode]}]

def image_to_base64(image_path):  
    with Image.open(image_path) as img:  
        buffer = BytesIO()  
        img.save(buffer, format='PNG')  
        img_data = buffer.getvalue()  
    return base64.b64encode(img_data).decode('utf-8')  
  
# 示例  
image_path = "/workspace/zecheng/ChatSydney-react-img/public/svgviewer-png-output.png"  
imageInput = image_to_base64(image_path)  

locale = 'zh-CN'

# chatbot = Chatbot.create(cookies=cookies, proxy=None, imageInput=imageInput)
# for _, response in chatbot.ask_stream(prompt=user_message, conversation_style=bot_mode, raw=True, webpage_context=context, search_result=True, locale=locale):
#     print(response)

async def sydney_process_message():    
    max_retries = 5  
    for i in range(max_retries + 1):  
        print(">>>>>>>>>>>>>>>")
        print(i)
        try:  
            chatbot = await Chatbot.create(cookies=cookies, proxy=None, imageInput=imageInput)    
              
            async for _, response in chatbot.ask_stream(prompt=user_message, conversation_style=bot_mode, raw=True, webpage_context=context, search_result=True, locale=locale):    
                yield response  
            break  
        except Exception as e:  
            if (  
                "Sorry, you need to login first to access this service." in str(e)  
                or "ServiceClient failure for DeepLeo" in str(e)  
                or "Cannot retrieve user status" in str(e)  
                or "Authentication failed" in str(e)  
                or "conversationSignature" in str(e)  
            ) and i < max_retries:  
                print("Retrying...", i + 1, "attempts.")  
                await asyncio.sleep(2)  
            else:  
                if i == max_retries:  
                    print("Failed after", max_retries, "attempts.")  
                print({"type": "error", "error": traceback.format_exc()})  
        finally:  
            if chatbot:  
                await chatbot.close()  
message = None
async def run_main():  
    async for response in sydney_process_message():
        # await ws.send_json(response)
        message = response
        # import pdb; pdb.set_trace()
  
asyncio.run(run_main())  

print(message)