source venv/bin/activate

#python botrun_gemini.py --project_id scoop-386004 \
#--location us-central1 \
#--model_name gemini-1.5-pro-preview-0409 \
#--text_prompt "請跟我講一個簡短的故事。" \
#--system_prompt "妳是講故事高手"

python botrun_gemini.py \
  --local_video_path "/Users/chiubowen/Desktop/color.mov" \
  --upload_path "users/BOTRUN_FOLDER/video/color.mov"
