from EdgeGPT.EdgeGPT import Chatbot



bot_mode = "creative"


chatbot = Chatbot.create(cookies=cookies, proxy=args.proxy, imageInput=imageInput)
async for _, response in chatbot.ask_stream(prompt=user_message, conversation_style=bot_mode, raw=True,
                                            webpage_context=context, search_result=True, locale=locale):