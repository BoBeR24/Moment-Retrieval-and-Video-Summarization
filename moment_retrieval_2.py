import torch
from lighthouse.models import QDDETRPredictor
from utils.expand_query import expand_query
from utils.video_splitter import split_video_ffmpeg
import os

device = "cuda" if torch.cuda.is_available() else "cpu"

video_path = "TVSum/video_25.mp4"

query = "The Kings mascot passes by waving."

# Split Video
chunks_dir = split_video_ffmpeg(video_path, chunk_size=150)


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
    i = 0

    for chunk_file in sorted(os.listdir(chunks_dir)):
        chunk_path = os.path.join(chunks_dir, chunk_file)

        result = model.predict(query, model.encode_video(chunk_path))
        prediction = {
            "start": result["pred_relevant_windows"][0][0] + (150*i),
            "end": result["pred_relevant_windows"][0][1] + (150*i),
            "score": result["pred_relevant_windows"][0][2]
        }

        if prediction["score"] > best_score:
            best_score = prediction["score"]
            best_result = prediction

        i += 1
    all_results.append(prediction)

print("\nALL RESULTS:")
for r in all_results:
    print(r)
