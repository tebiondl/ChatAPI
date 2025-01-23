## OBJECTIVE

The reason that this repository exist is to test how to build an API with a Text Generative AI ([GPT2](https://huggingface.co/meta-llama/gpt2)).

### DEPENDENCIES

To install the neccessary dependencies just run the next command:

    pip install -r requirements.txt

### HOW TO RUN?

To run the API locally use the next command in the terminal:

    python app.py

If all the dependencies have been correctly installed, in the terminal you should see that the service is running. In the terminal you should see 2 lines like this:

    * Serving Flask app 'app'
    * Debug mode: off

  
### CALL THE API

To call the API is very simple, just take the first link showed before (localhost:5000) and use it anywhere tou can call an API (Postman, Swagger, etc), for example using a python script like this (here the library requests is being used, if you want to use it, install it with *pip install requests*): 

```python
import requests
import json

endpoint = "generate"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
}

data = {"prompt": "Once upon a time"}
json_data = json.dumps(data)

response = requests.post("http://127.0.0.1:5000/" + endpoint, data=json_data, headers=headers)

print(response.json())
```

You can change the endpoint to any available in swagger (check next section) to see the different functions of the API. The code is available in the *test_api.py* script.

### CHECK DOCUMENTATION

The API documentation can be accessed going to localhost:5000/docs. It uses swagger.

Here there are some examples of how the api responds when asked to generate text:

    1.
    Prompt: "Tell me a joke"
    Answer: "Tell me a joke that should have been addressed sooner so that I can say it without sounding stupid!\" I smiled. \"I've already said it here...\" she said, and then held up a hand. \"And you say, 'I'm a"

    2.
    Prompt: "Once upon a time"
    Answer: "Once upon a time, the Great Ones and all the people of the Abyss were under the sway of the Lord of Light! It's time I went out as well!\n\n\"I have made my presence noticed. There are many things I'll"

And here is an example of the answers that have been saved inside the api.

```json
{
  "historic": [
    [
      "Tell me a joke",
      "Tell me a joke that should have been addressed sooner so that I can say it without sounding stupid!\" I smiled. \"I've already said it here...\" she said, and then held up a hand. \"And you say, 'I'm a"
    ],
    [
      "Tell me a joke",
      "Tell me a joke about this.\"\n\n\"It was your friend who had found your body.\"\n\n\"We'll be back.\"\n\n\"Okay.\"\n\nHarry stood and put on his robe. Gilderoy Lockhart was"
    ],
    [
      "Once upon a time",
      "Once upon a time, the Great Ones and all the people of the Abyss were under the sway of the Lord of Light! It's time I went out as well!\n\n\"I have made my presence noticed. There are many things I'll"
    ]
  ]
}
```