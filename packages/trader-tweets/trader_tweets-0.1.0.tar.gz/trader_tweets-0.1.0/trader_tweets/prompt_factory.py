import json
import os


def create_prompt_from_tweet(tweet_author, tweet_text, prompt_filename):
    res_path = os.path.join(os.path.dirname(__file__), '../res/prompts')
    prompt_path = os.path.join(res_path, prompt_filename)
    prompt_template_str = get_prompt_template_from_file(prompt_path)

    return build_prompt(prompt_template_str, tweet_author, tweet_text)


def get_training_tweets_from_file(training_tweets_path):
    # read json from training_tweets_path
    with open(training_tweets_path, 'r') as f:
        training_tweets = json.load(f)
    return training_tweets


def get_prompt_template_from_file(prompt_path):
    prompt_file = open(prompt_path, "r")
    prompt = prompt_file.read()
    prompt_file.close()
    # ignore lines with '#'
    all_lines = prompt.split('\n')
    lines_to_use = [line for line in all_lines if not line.startswith('#')]
    prompt = '\n'.join(lines_to_use)

    return prompt


def build_prompt(prompt_template, tweet_author, tweet_text):
    # replace author and text
    return prompt_template.format(author=tweet_author, tweet=tweet_text)
