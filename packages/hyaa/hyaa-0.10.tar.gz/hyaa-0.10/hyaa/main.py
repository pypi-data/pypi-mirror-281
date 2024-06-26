import click
import requests
import random

QUOTE_APIS = [
    "https://api.quotable.io/random",
    "https://zenquotes.io/api/random",
    "https://favqs.com/api/qotd",
]

RANDOM_QUOTES = [
    {
        "quote": "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "author": "Nelson Mandela"
    },
    # ... (other quotes remain the same)
]

def get_quote_from_api(api_url):
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "content" in data:  # Quotable API
            return data["content"], data["author"]
        elif "quote" in data and "body" in data["quote"]:  # FavQs API
            return data["quote"]["body"], data["quote"]["author"]
        elif isinstance(data, list) and data:  # ZenQuotes API
            return data[0]["q"], data[0]["a"]
        else:
            return None, None
    except:
        return None, None

def get_random_quote():
    # Try all APIs
    random.shuffle(QUOTE_APIS)
    for api_url in QUOTE_APIS:
        quote, author = get_quote_from_api(api_url)
        if quote and author:
            return quote, author

    # If all APIs fail, use a local quote
    random_quote = random.choice(RANDOM_QUOTES)
    return random_quote["quote"], random_quote["author"]

@click.command()
def random_quote():
    """Print a random quote."""
    quote, author = get_random_quote()
    click.echo(click.style(quote, fg="green", bold=True))
    if author:
        click.echo(click.style(f" - {author}", fg="yellow"))


def main():
    random_quote()

if __name__ == "__main__":
    main()