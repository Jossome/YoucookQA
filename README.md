# YoucookQA dataset
This repo is for collecting question-answer pairs for YoucookQA dataset. Please refer to our [arXiv paper](https://arxiv.org/abs/1812.00344) for details. This dataset will appear in WACV 2021.

## Files
- `generate_questions.py` is to generate 'when' questions along with answers.
- `generate_batches.py` generates batches for one-video version.
- `separate_segments_batches.py` generates batches for segments version.
- `.html` files copyrighted by Justin and Marc
- `./Results/*`
    - `split_val.py` splits the dataset into training, validation, testing sets.
    - `human_quiz.py` generate quiz for human test and check answers, get accuracy
    - `generate_json.py` assign type number and generate json based on original json file.
    - `get_dict.py` generate dictionary for questions and answers, and get the matrix.
    - `get_rest.py` get the HITs not completed yet.
    - `checkbox.py` annotate question types.
    - `statistics.py` get real statistics for the dataset
    - `csv_for_clean.py` generate batches for worker to clean the dataset
    - `auto_clean_numeric.py` cleans the numeric QAs
    - `collect.py` ensembles all cleaned work and get final json file
    - `type_intersect.py` calculates the intersection count among different types
- `data/*`
    - `.json` our QA dataset
    - `.txt` train/val/test split id

## Tasks
- [x] Interface for mturk
- [x] Collect data
- [x] Clean the data
- [x] Annotate checkbox for the 170 videos
- [x] Collect wiki introductions for each recipe
- [x] Human test
- [x] Split train-val-test like 6:2:2 
- Statistics
    - [x] Answer type statistics, for whole qa pairs and for each tag type
    - [x] Statistics for recipes
    - [x] tags per qa, qa per video 
    - [x] Statistics for detailed sub-types 
    - [x] Carefully choosed multiple choice alternatives
        - [x] Use similarity
        - [x] random pick
        - [x] use answer type (not qa type)

