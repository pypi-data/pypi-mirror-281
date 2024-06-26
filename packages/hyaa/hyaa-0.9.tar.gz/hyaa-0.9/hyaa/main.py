import click
import requests
import random

# List of quote APIs (you can add more)
QUOTE_APIS = [
    "https://api.quotable.io/random",
    "https://zenquotes.io/api/random",
    "https://favqs.com/api/qotd",
]

RANDOM_QUOTES = [
    {
        "quote":"The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "author":"Nelson Mandela"
    },
     {
        "quote": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs"
    },
    {
        "quote": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon"
    },
    {
        "quote": "Do not watch the clock. Do what it does. Keep going.",
        "author": "Sam Levenson"
    },
    {
        "quote": "You miss 100% of the shots you don't take.",
        "author": "Wayne Gretzky"
    },
    {
        "quote": "Whether you think you can or you think you can’t, you’re right.",
        "author": "Henry Ford"
    },
    {
        "quote": "The future belongs to those who believe in the beauty of their dreams.",
        "author": "Eleanor Roosevelt"
    },
    {
        "quote": "The purpose of our lives is to be happy.",
        "author": "Dalai Lama"
    },
    {
        "quote": "Get busy living or get busy dying.",
        "author": "Stephen King"
    },
    {
        "quote": "You have within you right now, everything you need to deal with whatever the world can throw at you.",
        "author": "Brian Tracy"
    }
]

def get_random_quote():
    # Choose a random API
    api_url = random.choice(QUOTE_APIS)
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()

        # Extract quote and author based on API structure
        if "content" in data:  # Quotable API
            quote = data["content"]
            author = data["author"]
        elif "quote" in data and "body" in data["quote"]:  # FavQs API
            quote = data["quote"]["body"]
            author = data["quote"]["author"]
        elif isinstance(data, list) and data:  # ZenQuotes API
            quote = data[0]["q"]
            author = data[0]["a"]
        else:
            return "Unable to parse quote from the API."

        return quote, author
    except Exception as e:
        # If API fails, use a random quote from RANDOM_QUOTES
        random_quote = random.choice(RANDOM_QUOTES)
        quote = random_quote["quote"]
        author = random_quote["author"]
        
        return quote, author


@click.command()
def random_quote():
    """Print a random quote."""
    message = "hyaa"
    person = "Kapil Bhandari"
    
    try:
        quote, author = get_random_quote()
        message = quote
        # click.echo(click.style(quote, fg="green", bold=True))
        if author:
            # click.echo(click.style(f" - {author}"))
            person = author
    except Exception as e:
        click.echo(click.style(message, fg="blue", bold=True))
        click.echo(click.style(f" - {person}"))

    finally:
        click.echo(click.style(message, fg="blue", bold=True))
        click.echo(click.style(f" - {author}"))
        
def main():
    random_quote()


if __name__ == "__main__":
    main()