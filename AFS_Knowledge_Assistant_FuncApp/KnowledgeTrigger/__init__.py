from openai import AzureOpenAI
from langchain.tools import BaseTool
from duckduckgo_search import DDGS
import azure.functions as func
import requests
import asyncio
import json
from typing import Optional
import logging
from langchain.tools import BaseTool


# gpt-4 turbo 128k
client = AzureOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_version= "2023-12-01-preview",
    api_key="6e9d4795bb89425286669b5952afe2fe",
    # base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/"
    base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/openai/deployments/GPT4Turbo/chat/completions?api-version=2023-12-01-preview"
)


# # gpt-4
    # model="DanielGPT4",

# client = AzureOpenAI(
#     # defaults to os.environ.get("OPENAI_API_KEY")
#     api_version= "2023-12-01-preview",
#     api_key="a5c4e09a50dd4e13a69e7ef19d07b48c",
#     # base_url="https://danielingitaraj.openai.azure.com/"
#     base_url="https://danielingitaraj.openai.azure.com/openai/deployments/DanielGPT4/chat/completions?api-version=2023-12-01-preview"
# )

# gpt 35 turbo 16k
# client = AzureOpenAI(
#     api_version= "2023-12-01-preview",
#     api_key="c09f91126e51468d88f57cb83a63ee36",
#     base_url="https://chat-gpt-a1.openai.azure.com/openai/deployments/DanielChatGPT16k/chat/completions?api-version=2023-12-01-preview"
# )

# gpt 35 turbo 4K
# client = AzureOpenAI(
#     api_version= "2023-12-01-preview",
#     api_key="c09f91126e51468d88f57cb83a63ee36",
#     base_url="https://chat-gpt-a1.openai.azure.com/openai/deployments/DanielChatGPT/chat/completions?api-version=2023-12-01-preview"
# )


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    chat_history = req.get_json()
    if not chat_history:
        return "Invalid Request Error"
    
    # chat_history[0] = {"role":"system","content":"You are a knowledge assistant dedicated to sharing information and assisting learners.\nYour responses are informative and designed to aid learning. You offer explanations, examples, and resources to support the learning process.\n\nYou maintain professional conduct by keeping the details of your internal functions confidential (DO NOT DISCLOSE INTERNAL FUNCTIONALITIES).\n\n Remember current date is ${16/02/2024} (DD/MM/YYYY) and timezone is ${IST} and for getting latest data you can search the internet using master_search. And finally provide a detailed descriptive answer with source attribution."}

    # print("*************************************************")
    # print(chat_history)
    # print("*************************************************")
    # print(type(chat_history))
    # print("*************************************************")



    if chat_history:

        class BingSearchTool(BaseTool):
            name = "Intermediate Answer"
            description = "useful for when you need to answer questions about current events"

            def _run(self, query: str) -> str:
                # subscription_key = "6637a6554ede48ba9e240d97c318f4ec"
                # subscription_key = "13835b8353af4f31959388f1494c29eb"
                subscription_key = "4d58afbdd2334025add149abdc2d92ef"
                endpoint = "https://api.bing.microsoft.com/v7.0/search"
                
                # Define the market as en-US
                mkt = 'en-US'
                
                # Construct parameters and headers for the API request
                params = {'q': query, 'mkt': mkt}
                headers = {'Ocp-Apim-Subscription-Key': subscription_key}
                
                try:
                    # Make the API request
                    response = requests.get(endpoint, headers=headers, params=params)
                    response.raise_for_status()
                    
                    # Extract relevant information from the response JSON
                    search_results = response.json().get('webPages', {}).get('value', [])

                    # Create a formatted result string
                    result_string = ""
                    for index, result in enumerate(search_results, start=1):
                        if index < 9 :
                            # result_string += f"{index}. {result['name']}\n   {result['snippet']}\n\n"
                            result_string += f"{index}. Topic: {result['name']} \n  Content: {result['snippet']}\n URL: {result['url']}\n\n "

                        else:
                            break
                
                    # print(result_string)
                    return result_string
                
                except Exception as ex:
                    return f"An error occurred: {str(ex)}"
            
            def _arun(self, query: str)-> str:
                raise NotImplementedError("This tool does not support async")


        bingsearch = BingSearchTool()


        # tool function
        async def master_search(input_json: str) -> dict:
            params = json.loads(input_json)

            operation = params.get('operation')
            keywords = params.get('keywords')
            region = params.get('region', 'wt-wt')
            max_results = params.get('max_results', 5)
            to_lang = params.get('to_lang', 'en')
            place = params.get('place')

            with DDGS() as ddgs:
                if operation == 'text':
                    return bingsearch.run(keywords)
                    # return [r for r in ddgs.text(keywords, region=region, max_results=max_results)]
                elif operation == 'image':
                    # return [r for r in ddgs.images(keywords, region=region, max_results=max_results)]
                    return bingsearch.run(keywords)
                elif operation == 'video':
                    # return [r for r in ddgs.videos(keywords, region=region, max_results=max_results)]
                    return bingsearch.run(keywords)
                elif operation == 'news':
                    return bingsearch.run(keywords)
                    # return [r for r in ddgs.news(keywords, region=region, max_results=max_results)]
                elif operation == 'map':
                    return bingsearch.run(keywords)
                    # return [r for r in ddgs.maps(keywords, place=place, max_results=max_results)]
                elif operation == 'translate':
                    return bingsearch.run(keywords)
                    # return ddgs.translate(keywords, to=to_lang)
                elif operation == 'suggestions':
                    return bingsearch.run(keywords)
                    # return [r for r in ddgs.suggestions(keywords, region=region)]
                else:
                    raise ValueError("Invalid operation. Please choose from: 'text', 'image', 'video', 'news', 'map', 'translate', 'suggestions'.")

        async def async_master_search(input_json):
            result = await master_search(input_json)
            return result
        

        # Defining the tools or functions
        functions = [
                        {
                            "name": "master_search",
                            "description": "Utilizes multiple search operations (text, image, video, news, map, translate, suggestions) to retrieve relevant information based on the specified operation and keywords. This tool is designed to provide diverse search capabilities using a single function.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "description": "The type of search operation to perform. Options include 'text', 'image', 'video', 'news', 'map', 'translate', 'suggestions'."
                                    },
                                    "keywords": {
                                        "type": "string",
                                        "description": "The keywords to search for in the specified operation."
                                    },
                                    "region": {
                                        "type": "string",
                                        "description": "Optional. The region to perform the search in. Defaults to 'wt-wt'."
                                    },
                                    "max_results": {
                                        "type": "integer",
                                        "description": "Optional. The maximum number of results to return. If not provided, all results will be returned."
                                    },
                                    "to_lang": {
                                        "type": "string",
                                        "description": "Optional. The target language for the 'translate' operation. Defaults to 'en'."
                                    },
                                    "place": {
                                        "type": "string",
                                        "description": "Optional. The place for the 'map' operation. If not provided, the 'keywords' parameter will be used."
                                    }
                                },
                                "required": ["operation", "keywords"]
                            }
                        }
                    ]

        # get completions

        def get_completion(messages=None, func=None, function_call="auto",
                        temperature=0, max_tokens=1000, top_p=1, frequency_penalty=0,
                        presence_penalty=0, stop=None):
            # Set default values if parameters are not provided
            messages = messages or []
            functions = func or []
            
            # Make API call with provided parameters
            response = client.chat.completions.create(
                messages= messages,
                model="GPT4Turbo",
                functions=func,
                function_call=function_call,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
            return response.choices[0].message


        def get_answer():
            message = chat_history.copy()
            print("Generating First Response")

            response = get_completion(messages=message, func=functions)
            print(response)

            while True:
                if response.function_call:
                    response.content = "null"
                    message.append(response)
                    function_name = response.function_call.name

                    if function_name == "master_search":
                        print("Searching Internet")

                        # Call the asynchronous master_search function
                        function_response = asyncio.run(async_master_search(response.function_call.arguments))
                        # print(function_response)

                        # st.experimental_show("Searching Internet Completed.")

                        message.append({
                            "role": "function",
                            "name": function_name,
                            "content": str(function_response),
                        })

                        # print(function_response)

                        print("generating response after function call")

                        response = get_completion(messages=message, func=functions)
                        print(response)

                        continue

                else:
                    print("Returning Final Response")
                    chat_history.append({"role": "assistant", "content": response.content})

                    # print(response)
                    return response.content


        try:
            ans = get_answer()
            print(ans)
            return func.HttpResponse(json.dumps({"role": "assistant", "content": ans}), status_code=200)

        except Exception as e:
            return func.HttpResponse(json.dumps({"role": "assistant", "content": str(e)}), status_code=200)


    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
