"""
Compress mp4 file
"""
original_file="$*"

ffmpeg -i "$original_file" tmp.mp4
ffmpeg -i tmp.mp4 -vf "scale=960:-2" tmp_small.mp4
ffmpeg -i tmp_small.mp4 -crf 10 ~/Desktop/compressed.mp4

rm tmp.mp4 tmp_small.mp4
