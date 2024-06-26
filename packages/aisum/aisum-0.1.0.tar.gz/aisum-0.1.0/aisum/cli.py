import click
import sys
from .openai_api import summarize_text

@click.command()
def main():
    """Simple CLI tool to summarize text using OpenAI"""
    input_text = sys.stdin.read()
    summary = summarize_text(input_text)
    click.echo(summary)

if __name__ == '__main__':
    main()
