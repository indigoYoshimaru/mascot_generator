from diffusers import AutoPipelineForText2Image
import torch

model_name = "kandinsky-community/kandinsky-2-2-decoder"
lora_model_path = "models/weight/kandinsky-2-2-logo/checkpoint-2500"
image_save_path = ".experiments/monkey.png"

pipeline = AutoPipelineForText2Image.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    use_safetensors=True,
)

prompt = "a large, stunning, cool lighting, funky background, clear, colorful, animated smiley monkey wearing hat, shirt, and dark glasses, jewelries as a mascot, with One Mount logo in the shape of rounded Mobius strip on the shirt"
# prompt = "snake eye, greenish, Emil Melmoth rounded Mobius strip"
# negative_prompt = "easynegative, (low quality, worst quality:1.4), bad anatomy, bad composition, out of frame, duplicate, watermark, signature, text"

pipeline.unet.load_attn_procs(lora_model_path)
pipeline.to("cuda")

image = pipeline(
    prompt,
    prior_guidance_scale=1.0,
    height=768,
    width=512,
    num_inference_steps=50,
).images[0]

image.save(image_save_path)
