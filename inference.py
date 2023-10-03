import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import base64
import pandas as pd
import os
import time

async def main():

    model_name = "bing_short_balanced"
    if "balanced" in model_name:
        conversation_style = ConversationStyle.balanced
    elif "precise" in model_name:
        conversation_style = ConversationStyle.precise
    else:
        conversation_style = ConversationStyle.creative
    
    bard_error = "Temporarily unavailable due to traffic or an error in cookie values."
    version = "1_4"
    rerun_ids = [] # ['v1_137']

    if 'bard' in model_name or 'bing' in model_name:
        save_full_reponse = True
    else:
        save_full_reponse = False
    results_path = f'/home/weihao/data/mmeval/results/mmeval_{version}_{model_name}.json'
    if save_full_reponse:
        results_path_full = f'/home/weihao/data/mmeval/results/mmeval_{version}_{model_name}_full.json'
    image_folder = f"/home/weihao/data/mmeval/cemm_{version}_1m"
    data_csv = f"/home/weihao/data/mmeval/mmeval_{version}.csv"

    data = pd.read_csv(data_csv)


    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            results = json.load(f)
    else:
        results = {}

    if save_full_reponse:
        if os.path.exists(results_path_full):
            with open(results_path_full, 'r') as f:
                results_full = json.load(f)
        else:
            results_full = {}

    # time.sleep(60)
    for i in range(len(data)):
        id = data.loc[i, 'id']
        if id in results:
            if "bard" in model_name:
                is_bard_error = (bard_error in results[id])
            else:
                is_bard_error = False
            if not is_bard_error and id not in rerun_ids:
                continue
        # time.sleep(60)
        imagename = data.loc[i, 'imagename']
        category = data.loc[i, 'category']
        img_path = os.path.join(image_folder, imagename)
        prompt = data.loc[i, 'question']
        prompt = prompt.strip()
        if 'short' in model_name:
            prompt = prompt + " (Generate a short and concise response.)"
        print(id)
        print(f"\nPrompt: {prompt}")
        # load sample image

        cookies = json.loads(open("bing_cookies_weihao.json", encoding="utf-8").read())
        with open(img_path, "rb") as img_file:
            image = base64.b64encode(img_file.read())
        bot = await Chatbot.create(cookies=cookies, imageInput=image) # Passing cookies is "optional", as explained above
        bing_answer = await bot.ask(prompt=prompt, conversation_style=conversation_style, simplify_response=True)
        response = bing_answer['text']
        print(f"Response: {response}")
        results[id] = response        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=4)
        if save_full_reponse:
            full_response = bing_answer
            results_full[id] = full_response
            with open(results_path_full, 'w') as f:
                json.dump(results_full, f, indent=4)
        await bot.close()
        break


if __name__ == "__main__":
    asyncio.run(main())



# cookies = json.loads(open("./path/to/cookies.json", encoding="utf-8").read())  # might omit cookies option
# bot = await Chatbot.create(cookies=cookies)