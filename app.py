from flask import Flask, request, jsonify, render_template, send_from_directory
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import os
import torch


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

'''
Request Type: POST
Input Data: {"prompt": "prompt for the generative model"}
Output Data: {"generated_text": "answer of the model"}
'''
@app.route("/generate", methods=["POST"])
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
            
        return jsonify({"generated_text": generated_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


'''
Request Type: POST
Input Data: {"*": "Any existant parameter for an specific model configuration"}
Output Data: {"A good message if the configuration was applied"}
'''
@app.route("/change_config", methods=["POST"])
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
    
@app.route('/docs')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
