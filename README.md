# Exploring /r/kpop discussion

> :warning: Project is under active development. Details below are more notes in progress rather than documentation for public consumption

## Introduction

Do /r/kpop commenters talk differently about male vs. female groups?

Initial exploration of this question:

- Identify submissions on 2 all-male groups, 2 all-female groups
- Collect their comments
- Contrast comments in general to "typical" reddit language (using /r/funny as a standard)
- Contrast comments on male group vs female group
  - Separate out into comments for different groups
    - e.g. What adjectives are most associated with which groups?
  - What sort of emojis are used?

### First-Time Set-Up

Create `/data/` and `/data/comments/`.

```bash
mkdir data
mkdir data/comments
conda env create -f environment.yml
conda activate gendered-discussion
python
```

Within Python interpreter

```python
import nltk
nltk.download('stopwords')
```

Run `data_collection.ipynb`

### TODO

- [ ] Add econjobrumors gender paper to references

### Data Collection

Using Pushshift to get reddit comments

See [Pushshift's GitHub API README](https://github.com/pushshift/api)

> Search for the most recent comments mentioning the word "science" within the subreddit /r/askscience
>
> `https://api.pushshift.io/reddit/search/comment/?q=science&subreddit=askscience`

Retrieve all comment ids for a submission object

`https://api.pushshift.io/reddit/submission/comment_ids/{base36_submission_id}`

[New to Pushshift FAQ](https://www.reddit.com/r/pushshift/comments/bcxguf/new_to_pushshift_read_this_faq/)

[Pushshift Reddit API v4.0 Documentation](https://reddit-api.readthedocs.io/en/latest/#)

! Pushshift created [a tool for more user-friendly search of reddit submissions and comments](https://redditsearch.io/). (What's the rate limit?)

### Related Works (Incomplete)

- "A Community of Curious Souls: An Analysis of Commenting Behavior on TED Talks Videos" (Tsou, Thelwall, Mongeon, and Sugimoto, 2014)
- "YouTube science channel video presenters and comments: female friendly or vestiges of sexism?" (Thelwall and Mas-Bleda, 2018)
- "Shirtless and dangerous: Quantifying linguistic signals of gender bias in an online fiction writing community." (Fast, Vachovsky, and Bernstein, 2016)
- "Using language models to quantify gender bias in sports journalism" (Fu, Danescu-Niculescu-Mizil, Lee, 2016)

> :bulb: Look at /r/science instead and how it discusses race/gender?
