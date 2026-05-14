# Moment-Retrieval-and-Video-Summarization

This project was done as part of an assignment for the Computer Vision course at Maastricht University (Group 7, 2026). It implements a full pipeline from video annotation to highlights summarisation using Vision-Language Models, Large Language Models, and pre-trained moment retrieval models.

---

## Repository Structure

```
├── Annotations/              # Human-annotated ground truth events (CSV/TXT per video)
├── Descriptions/             # VLM + LLM output JSONs (video_{id}.json)
├── Evaluations/              # Embedding similarity eval results (video_{id}_eval_annot.json)
│                             # Timestamp IoU eval results     (video_{id}_eval_time.json)
├── Timestamps/               # Moment retrieval predictions   (video_{id}_with_predictions.json)
├── TVSum/                    # Raw video files (video_25.mp4 … video_28.mp4) — not tracked
├── model_weights/            # Pre-trained model checkpoints  — not tracked, see below
├── processed_videos/         # Intermediate video files produced by MR notebooks — not tracked
├── additional_materials/     # Assignment brief and supporting documents
├── utils/                    # Shared utility scripts
├── vlm_pipeline.ipynb                  # Stage 1: VLM frame description generation
├── llm_pipeline.ipynb                  # Stage 2: LLM salient event extraction
├── evaluation_annotations_pipeline.ipynb  # Stage 3: Embedding similarity evaluation
├── moment_retrieval_1.ipynb            # Stage 4: CG-DETR moment retrieval
├── moment_retrieval_2.py               # Stage 4: QD-DETR moment retrieval
├── evaluation_timestamps_pipeline.ipynb   # Stage 5: Timestamp IoU evaluation
└── .gitignore
```

---

## Pipeline Overview

```
Video frames → VLM → descriptions → LLM → events → [embedding eval vs annotations]
                                                  ↓
                                         Moment Retrieval (CG-DETR / QD-DETR)
                                                  ↓
                                         Timestamps → [IoU eval vs annotations]
                                                  ↓
                                         Video Summary (stitching)
```

---

## Setup

### Dependencies

```bash
pip install torch transformers sentence-transformers
pip install opencv-python pillow pandas numpy matplotlib seaborn scikit-learn
pip install av num2words
```

The VLM pipeline requires a CUDA-capable GPU. The LLM pipeline requires [Ollama](https://ollama.com) running locally:

```bash
ollama run llama3.2
```

### Videos

Download the TVSum videos assigned to Group 7 (videos 25–28) and place them in `TVSum/` as `video_25.mp4`, `video_26.mp4`, `video_27.mp4`, `video_28.mp4`.

### Model Weights

Download the pre-trained model checkpoints and place them in `model_weights/`. Required:

- **CG-DETR:** `clip_slowfast_cg_detr_qvhighlight.ckpt` — [TODO: add download link]
- **QD-DETR:** [TODO: add download link]

---

## Running the Pipeline

Run the notebooks in order:

| Step | Notebook | Description |
|------|----------|-------------|
| 1 | `vlm_pipeline.ipynb` | Samples frames from each video and generates descriptions using SmolVLM2-2.2B-Instruct across 3 prompt types × 3 frame counts |
| 2 | `llm_pipeline.ipynb` | Extracts structured salient event lists from VLM descriptions using Llama 3.2 |
| 3 | `evaluation_annotations_pipeline.ipynb` | Evaluates LLM events against human annotations using sentence embedding cosine similarity |
| 4 | `moment_retrieval_1.ipynb` | Runs CG-DETR on each event as a text query; supports chunking and speed-up strategies for videos longer than 150s |
| 4 | `moment_retrieval_2.py` | Runs QD-DETR — [TODO: add usage instructions] |
| 5 | `evaluation_timestamps_pipeline.ipynb` | Evaluates predicted timestamps against ground truth using IoU, coverage, precision, and F1 |

Each notebook skips already-completed entries, so they can be safely interrupted and re-run.

---

## Annotations

Human annotations are stored in `Annotations/GroundTruthVideo{id}.txt` in the format:

```
annotation, timestamp, subjectivity_rating
```

Timestamps are formatted as `MM:SS - MM:SS`. Subjectivity ratings range from `-2` (highly subjective) to `2` (objectively essential).

---

## Results

TODO: add summary of best-performing configurations and key findings.

---

## Authors

TODO: add group member names.

---

## Course

Computer Vision — Maastricht University, 2026  
Supervisor: Mirela Popa
