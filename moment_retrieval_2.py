import torch
from lighthouse.models import QDDETRPredictor
from utils.helper_methods import split_video_ffmpeg, create_speedup_video
import os

device = "cuda" if torch.cuda.is_available() else "cpu"

# Create 2x video
video_path_25 = "TVSum/video_25_2x.mp4"
# video_path_25 = create_speedup_video(video_path_25, speed=2)
video_path_26 = "TVSum/video_26.mp4"
video_path_27 = "TVSum/video_27_3x.mp4"
# video_path_27 = create_speedup_video(video_path_27, speed=3)
video_path_28 = "TVSum/video_28_2x.mp4"
# video_path_28 = create_speedup_video(video_path_28, speed=2)

# Load Model
# Weights downloaded from https://zenodo.org/records/13960580
model = QDDETRPredictor(
    'model_weights/clip_qd_detr_qvhighlight.ckpt',
    device=device,
    feature_name="clip"
)

# Events / Queries
events = ["A person walking down a street in a city, passing by various buildings and shops",
          "A person sitting on the ground, wearing earphones and looking at something in their hands",
          "A group of people gathered around a banner, with one person holding a microphone",
          "The video then shows a group of people standing on a beach, with a large building in the background",
          "A person lying on a bed, holding a camera",
          "A group of people playing in a dirt field, with a large building in the background"]

all_results = []
for query in events:

    # Predicting...
    best_prediction = None
    best_score = -1

    result = model.predict(query, model.encode_video(video_path_25))
    prediction = {
        "start": result["pred_relevant_windows"][0][0],
        "end": result["pred_relevant_windows"][0][1],
        "score": result["pred_relevant_windows"][0][2]
    }

    if prediction["score"] > best_score:
        best_score = prediction["score"]
        best_result = prediction

    all_results.append(best_result)

print("\nALL RESULTS:")
for r in all_results:
    print(r)
