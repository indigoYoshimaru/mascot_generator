export TRAIN_DIR="OM_logos"
export OUTPUT_DIR="models/weight/kandinsky-2-2-logo-prior"

accelerate launch diffusers/examples/kandinsky2_2/text_to_image/train_text_to_image_lora_prior.py \
    --train_data_dir=$TRAIN_DIR \
    --caption_column="text" \
    --resolution=512 \
    --train_batch_size=2 \
    --mixed_precision="fp16" \
    --max_train_steps=2500 \
    --learning_rate=1e-04 \
    --max_grad_norm=1 \
    --lr_scheduler="constant" \
    --lr_warmup_steps=0 \
    --seed=42 \
    --rank=4 \
    --output_dir=${OUTPUT_DIR} \
    --report_to="tensorboard"

