## OBJECTIVE

The reason that this repository exist is to test how to build an API with a Text Generative AI ([GPT2](https://huggingface.co/meta-llama/gpt2)).

### DEPENDENCIES

To install the neccessary dependencies just run the next command:

    pip install -r requirements.txt

### HOW TO RUN?

To run the API locally use the next command in the terminal:

    python app.py

If all the dependencies have been correctly installed, in the terminal you should see that he service is running. In the terminal you should see 2 addreses like this:

    * Running on http://127.0.0.1:5000
    * Running on http://192.168.1.76:5000
  
### CALL THE API

To call the API is very simple, just take the first link showed before (http://127.0.0.1:5000) and use it anywhere tou can call an API, for example using a python script like this (here the library requests is being used, if you want to use it installit with *pip install requests*): 

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

The API documentation can be accessed going to http://127.0.0.1:5000/docs. It uses swagger.
