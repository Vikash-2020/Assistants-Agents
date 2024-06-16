import logging
from openai import AzureOpenAI
import requests
import json
import azure.functions as func



# gpt-4 turbo 128k
client = AzureOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_version= "2023-12-01-preview",
    api_key="6e9d4795bb89425286669b5952afe2fe",
    # base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/"
    base_url="https://danielingitaraj-gpt4turbo.openai.azure.com/openai/deployments/GPT4Turbo/chat/completions?api-version=2023-12-01-preview"
)

# # gpt-4
# client = AzureOpenAI(
#     # defaults to os.environ.get("OPENAI_API_KEY")
#     api_version= "2023-12-01-preview",
#     api_key="a5c4e09a50dd4e13a69e7ef19d07b48c",
#     # base_url="https://danielingitaraj.openai.azure.com/"
#     base_url="https://danielingitaraj.openai.azure.com/openai/deployments/DanielGPT4/chat/completions?api-version=2023-12-01-preview"
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
        
        # tool
        def Scraper(input_data):
            # endpoint_url = "https://dataformatterllm.azurewebsites.net/api/TriggerFormatter?code=LEvekwwQT5SNHM2ibQN9prC1oWbVENiUGTqlWXjvA98tAzFuoJFCmQ=="  # Replace with your actual endpoint URL
            endpoint_url = "https://webscraptool.azurewebsites.net/"  # Replace with your actual endpoint URL
            print("calling Data formatter function")
            try:
                response = requests.post(endpoint_url, json=input_data)
                # print(response)
                if response.status_code == 200:
                    response_data = response.json()
                    return response_data
                else:
                    return None

            except Exception as e:
                print(f"An error occurred while making the request: {e}")
                return None


        # Defining the tools or functions
        functions = [
            {
                "name": "Scraper",
                "description": "Use the Scraper function to extract data by sending a list of URLs and a search keyword to a specified endpoint URL.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_data": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "A list of URLs from which data will be extracted."
                                },
                                "keyword": {
                                    "type": "string",
                                    "description": "The search keyword used to extract specific data from the URLs."
                                }
                            },
                            "required": ["url", "keyword"],
                            "description": "The input data containing URLs and a search keyword for data extraction."
                        }
                    },
                    "required": ["input_data"]
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

            # print(message)
            print("Generating First Response")

            response = get_completion(messages= message, func= functions)
            # print(response)

            while True:
                if response.function_call:
                    # st.write()
                    response.content = "null"
                    message.append(response)
                    function_name = response.function_call.name
                    if function_name == "Scraper":
                        print("Scraping Url")

                        function_response =  str(Scraper(json.loads(response.function_call.arguments)["input_data"]))

                        message.append(
                            {
                                "role": "function",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                        # print(function_response)

                        print("generating response after function call")

                        response = get_completion(messages= message, func= functions)
                        # print(response)
                        continue
                else:
                    print("Returning Final Response")
                    chat_history.append({"role": "assistant", "content": response.content})
                    # print(response)
                    return response.content
                
        try:
            ans = get_answer()
            # print(ans)
            return func.HttpResponse(json.dumps({"role": "assistant", "content": ans}), status_code=200)

        except Exception as e:
            return func.HttpResponse(json.dumps({"role": "assistant", "content": str(e)}), status_code=200)


    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
