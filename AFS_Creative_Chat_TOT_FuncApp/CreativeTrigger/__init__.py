import logging
import azure.functions as func
import time
import requests
import json
from openai import AzureOpenAI
from langchain.tools import BaseTool


# gpt-4 turbo 128k
client = AzureOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_version= "2024-02-15-preview",
    api_key="6e9d4795bb89425286669b5952afe2fe",
    # base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/"
    base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/openai/deployments/GPT4Turbo/chat/completions?api-version=2024-02-15-preview"
)

# # gpt-4
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
                subscription_key = "13835b8353af4f31959388f1494c29eb"
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
                        if index < 6 :
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

        def get_data(query):
            # print("Sending request to Creative Tool.")
            endpoint_url = "https://afscreativewritingassistant.azurewebsites.net/api/Creative_Trigger?code=iL5YhIkNHddNhV0jH06pfu7LY-gbrlbdZvasJWlj2iPuAzFuPd9gog=="  # Replace with your actual endpoint URL

            print(type(query))
            print(query['query'])

            # Define the data payload for the POST request
            data = {
                "question": query['query']
            }

            # print(f"Data: {data}")
            # data = json.dumps(data)
            try:
                # Send a POST request to the Azure Web App Service
                response = requests.post(endpoint_url, json=data)

                # Check if the request was successful (HTTP status code 200)
                if response.status_code == 200:
                    # print("Successfully called Creative tool")
                    # Parse the JSON response from the server
                    response_data = response.json()
                    # return response_data["extracted_data"]
                    print("Returning data to LLM")
                    return response_data["Output"]
                else:
                    print(f"Request failed with status code {response.status_code}")
                    return None

            except Exception as e:
                # print(response.content)
                print(f"An error occurred while making the request: {e}")
                return None
            

        # Defining the tools or functions
        functions = [
                        {
                            "name": "creative_tool",
                            "description": "Utilize the creative tool AI agent for all writing task, equipped with the latest data and internet access, to intelligently solve various legal writing tasks by sending a query string for resolution.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The query or task to be solved by the creative tool AI agent."
                                    }
                                },
                                "required": ["query"]
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
                # model="DanielGPT4",
                # model="DanielChatGPT16k",
                # model="DanielChatGPT",
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
            message  = chat_history.copy()
            # print(message)
            print("Generating First Response")

            response = get_completion(messages= message, func= functions)


            while True:
                if response.function_call:

                    response.content = "null"
                    message.append(response)
                    function_name = response.function_call.name
                    if function_name == "creative_tool":
                        print("Calling Creative tool")
                        function_args = json.loads(response.function_call.arguments)
                        print(function_args)
                        function_response =  get_data(function_args)

                        message.append(
                            {
                                "role": "function",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                        print(message)

                        print("generating response after function call")
                        # response = get_completion(messages= message, functions= functions)
                        response = get_completion(messages= message, func= functions)
                        print(response)
                        continue
                else:
                    print("Returning Final Response")
                    chat_history.append({"role": "assistant", "content": response.content})
                    print(response)
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
