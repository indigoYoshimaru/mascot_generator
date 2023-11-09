from diffusers import AutoPipelineForText2Image
import torch

model_name = "kandinsky-community/kandinsky-2-2-decoder"
image_save_path = ".experiments/mascot-1.png"

pipeline = AutoPipelineForText2Image.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    use_safetensors=True,
).to("cuda")


prompt = "a cool llama as a mascot stunning, warm lighting, funny background, clear, colorful, animated drawing, with black glasses"
# negative_prompt = "easynegative, (low quality, worst quality:1.4), bad anatomy, bad composition, out of frame, duplicate, watermark, signature, text"

image = pipeline(
    prompt,
    prior_guidance_scale=1.0,
    height=768,
    width=512,
    num_inference_steps=50,
).images[0]

image.save(image_save_path)
