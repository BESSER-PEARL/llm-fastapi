import os
import time
import uuid

from fastapi import FastAPI, HTTPException
from huggingface_hub import login
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the LLM model from environment variable
LLM_NAME = os.getenv("LLM_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

if not LLM_NAME:
    raise ValueError("Environment variablre 'LLM_NAME' is not set.")

if HF_TOKEN:
    login(HF_TOKEN)

# Initialize tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(LLM_NAME)
    model = AutoModelForCausalLM.from_pretrained(LLM_NAME)
except Exception as e:
    raise ValueError(f"Failed to load model '{LLM_NAME}': {e}")

# Initialize FastAPI app
app = FastAPI()


# Define request and response models
class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 50
    temperature: float = 0.7
    top_p: float = 1.0


class CompletionResponse(BaseModel):
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: list


@app.post("/v1/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest):
    if request.model != LLM_NAME:
        raise HTTPException(status_code=400, detail="Model not supported.")

    # Generate response using the Hugging Face model
    input_ids = tokenizer.encode(request.prompt, return_tensors="pt")
    outputs = model.generate(
        input_ids,
        max_length=request.max_tokens + input_ids.shape[1],
        temperature=request.temperature,
        top_p=request.top_p,
        do_sample=True,
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Prepare API response
    response = CompletionResponse(
        id=str(uuid.uuid4()),
        created=int(time.time()),
        model=LLM_NAME,
        choices=[
            {
                "message": {
                    "role": "assistant",
                    "content": generated_text
                },
                # "index": 0,
                # "logprobs": None,
                "finish_reason": "length", # or stop
            }
        ],
    )
    return response
