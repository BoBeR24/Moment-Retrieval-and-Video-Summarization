1.  OK (D*) Video Annotator 1
    OK (L*) Video Annotator 2
->    (L) Cohen's Kappa
2.  -
3.  OK (E*) VLM w/out timestamps
        (E*) output to list
->    (E*) VLM with timestamps
        (E*) output to list
    (E*) Multiple Prompts for Comparison
    (E*) Compare Annotations to VLM Output
4.  OK (L*) Moment Retrieval Model 1
        (L*) Multiple Scoring + Merging
    OK (D*) Moment Retrieval Model 2
        (D*) Multiple Scoring + Merging
5.  (E) Jaccard Metric 
        (E) Model 1
        (E) Model 2
    (E) Other Metric?
6.  (TBD) Stitching Outputs
        (TBD) Model 1
        (TBD) Model 2
    (TBD) Is it good based on 
        Relevance
        Coverage
        Conciseness
        Coherence

* = Do before presentation
    
(D E L) Presentation
Report
    (L) Cohen's Kappa
    (E) VLMs
    (D L) Moment Retrieval
    (E) Metrics 
    (D L) Annotations + Comments on why you picked those annotations
    (D L) Stitched Videos

1. Video annotations:
    - (L) Kappa
    - (L) Find the ground truth
    - (D) Comments on picking given moments
3. (E) VLM/LLM
    - Automate, generate structured outputs for all videos
    - Different prompts evaluation
    - Embedding evaluations
4. (D) Moment Retrieval
    - Trying different approaches like sampling + comparing
5. (TBD) Jaccard Metric
6. (L) Stitching
    - Automation, abstraction
7. README + refactoring into reusable chunks/final pipeline notebook?