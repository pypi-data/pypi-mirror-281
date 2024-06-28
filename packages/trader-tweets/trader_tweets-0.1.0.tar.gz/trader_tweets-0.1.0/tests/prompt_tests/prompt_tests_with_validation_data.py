import json
import unittest

from parameterized import parameterized

from trader_tweets.prompt_factory import create_prompt_from_tweet
from trader_tweets.service.classifier.gpt_classifier import (classify_prompt, DEFAULT_PROMPT_TEMPLATE,
                                                             DEFAULT_BASE_GPT_MODEL)
from trader_tweets.strategy.response_parsers import parse_word_response
from trader_tweets.trade_tweet_job import TweetType

reference_tweets = {
    TweetType.TRADE: [],
    TweetType.PREDICTION: [],
    TweetType.NOT_INTERESTING: []
}

parameterized_test_cases_trade = map(
    lambda tweet_id: [tweet_id, TweetType.TRADE], reference_tweets[TweetType.TRADE]
)
parameterized_test_cases_alpha = map(
    lambda tweet_id: [tweet_id, TweetType.PREDICTION], reference_tweets[TweetType.PREDICTION]
)
parameterized_test_cases_not_interesting = map(
    lambda tweet_id: [tweet_id, TweetType.NOT_INTERESTING], reference_tweets[TweetType.NOT_INTERESTING]
)

VALIDATION_CASES_FILE = '../../res/training/tweet-type/classified-training-tweets-set-3_prepared_valid (2).jsonl'

GPT_MODEL = DEFAULT_BASE_GPT_MODEL


def read_test_cases_fom_validation_file() -> [(str, TweetType)]:
    # test cases are in the form { 'prompt': '...', 'completion': '...' }
    with open(VALIDATION_CASES_FILE, 'r') as f:
        for line in f:
            test_case = json.loads(line)
            parsed_tweet_type = parse_word_response(test_case['completion'])
            prompt = test_case['prompt']
            # todo: fix this pre-update stuff
            # if not USING_FINE_TUNING:
            # prepend gpt_classifier chosen prompt
            standard_prompt = DEFAULT_PROMPT_TEMPLATE
            standard_prompt_str = create_prompt_from_tweet(None, None, standard_prompt.filename)
            prompt = standard_prompt_str + prompt
            yield prompt, parsed_tweet_type


class PromptTestsValidationSet(unittest.TestCase):

    @parameterized.expand(read_test_cases_fom_validation_file())
    def test_validation_set(self, prompt, expected_tweet_type):
        self.check_tweet_type(prompt, expected_tweet_type)

    def check_tweet_type(self, prompt, expected_tweet_type):
        classification = classify_prompt(prompt, GPT_MODEL)
        self.assertEqual(expected_tweet_type, classification)
