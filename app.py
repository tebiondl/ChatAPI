from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import os
import torch
from database import init_db, insert_question, get_questions
from dotenv import load_dotenv
load_dotenv()

try:
    # Load model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "gpt2"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id, torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer, 
        device=0 if device == "cuda" else -1
    )
except Exception as e:
    raise RuntimeError(f"Error loading the model: {e}")

# Start flask app
app = Flask(__name__)

try:
    # Obviously in production, this key must be secret, but for this example it will be public
    app.config["JWT_SECRET_KEY"] = os.getenv("MY_SECRET_KEY")
    jwt = JWTManager(app)
    
except KeyError:
    raise RuntimeError("JWT_SECRET_KEY environment variable not set")

# Initialize the database
try:
    init_db()
except Exception as e:
    raise RuntimeError(f"Error initializing the database: {e}")

'''
Request Type: POST
Input Data: {"prompt": "prompt for the generative model"}
Output Data: {"generated_text": "answer of the model"}
'''
@app.route("/generate", methods=["POST"])
@jwt_required()
def generate_text():
    try:
        # Get data from the request
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Invalid request, 'prompt' is required"}), 400
        
        prompt = data["prompt"]
        if not isinstance(prompt, str) or not prompt.strip():
            return jsonify({"error": "Prompt must be a non-empty string"}), 401
    
        outputs = pipe(prompt, num_return_sequences=1)
        generated_text = outputs[0]["generated_text"]
        
        # Save the question in the database
        insert_question(prompt, generated_text)   
            
        return jsonify({"generated_text": generated_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


'''
Request Type: GET
Output Data: {"historic": [["prompt", "answer of the model"], ["prompt2", "second answer of the model"], ...]}
'''
@app.route("/historic", methods=["GET"])
@jwt_required()
def get_historic():
    try:
        # Get data from the database
        historic = get_questions()
            
        return jsonify({"historic": historic})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

'''
Request Type: POST
Input Data: {"*": "Any existant parameter for an specific model configuration"}
Output Data: {"A good message if the configuration was applied"}
'''
@app.route("/change_config", methods=["POST"])
@jwt_required()
def change_config():
    global pipe, model, tokenizer
    try:
        # Get data from the request
        data = request.get_json()

        # It checks if the model config has this specific configutrations
        for key, value in data.items():
            if hasattr(model.config, key):
                setattr(model.config, key, value)
            else:
                return jsonify({"error": f"Invalid config key: {key}"}), 400
            
        # Refresh pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer, 
            device=0 if device == "cuda" else -1
        )
            
        return jsonify("Applied Configuration")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/login', methods=['GET'])
def login():
    
    #For simplicity, this method will not check any credentials, just give the token
    
    access_token = create_access_token(identity="admin")
    return jsonify(access_token=access_token)
    
@app.route('/docs')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
