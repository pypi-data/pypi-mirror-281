import os

from openai import OpenAI

from trader_tweets_core.service.cache_service import memoize_cache

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


# tweet type
ADA_FT_V1 = "ada:ft-personal-2022-08-25-11-31-34"
CURIE_FT_V1 = "curie:ft-personal-2022-08-25-11-11-27"
CURIE_FT_V1_2 = "curie:ft-personal-2022-08-26-11-08-47"
DAVINCI_FT_V1 = "davinci:ft-personal-2022-08-25-11-43-52"
ADA_FT_V2 = "ada:ft-personal-2022-09-01-10-53-03"
CURIE_FT_V2 = "curie:ft-personal-2022-09-01-11-18-38"
CURIE_FT_V3 = "curie:ft-personal-2023-02-27-09-03-25"

# 2024
BABBAGE = "ft:babbage-002:personal:march-02:8yCTascS"

# open-close
OPEN_CLOSE_10 = "davinci:ft-personal-2023-02-26-05-50-11"
OPEN_CLOSE_50 = "davinci:ft-personal-2023-02-26-09-45-57"


@memoize_cache
def ask_gpt_for_response(prompt, max_response_tokens=5, model="gpt-3.5-turbo-instruct"):
    # check if the tweet is a trade using gpt-3
    gpt_response = client.completions.create(
        model=model,
        prompt=prompt,
        max_tokens=max_response_tokens,
        temperature=0.0,
        top_p=1,
        frequency_penalty=0.0)

    response_text = gpt_response.choices[0].text
    # trim string
    trimmed_response = response_text.strip()
    return trimmed_response
