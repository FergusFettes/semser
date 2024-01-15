from semanticscholar import SemanticScholar
import typer
import rich
import requests
from pathlib import Path


sch = SemanticScholar()
app = typer.Typer()


@app.command()
def main(query: str, limit: int = 10):
    papers = sch.search_paper(query, limit=limit)
    for i in range(limit):
        paper = papers[i]
        title = paper['title']
        date = paper['publicationDate']
        authors = ", ".join([author['name'] for author in paper['authors']])
        citations = paper['citationCount']
        # This will be a color, used in the shell
        if paper['openAccessPdf']:
            open_status = paper['openAccessPdf']['status'].lower()
            open_status = "green" if open_status in ["green", "gold", "hybrid"] else "red"
            rich.print(paper['openAccessPdf'])
        else:
            open_status = "red"
        rich.print(
            f"{i}: "
            f"({citations}) "
            f"{title}, "
            f"[i]{authors[:60]}[/i], "
            f"{date}, "
            f"[{open_status}]Open[/{open_status}]"
        )

    # Read in some values. If they are numbers, get those papers
    results = typer.prompt("Papers to retrieve (csl: 1,2,3 etc): ")
    if not results:
        return

    results = results.split(',')

    typer.echo(f"\nDownloading {results}")
    for result in results:
        if paper['openAccessPdf']:
            download(papers[int(result)]['openAccessPdf']['url'])
        else:
            typer.echo("No open access PDF available for this paper.")


def download(url):
    """
    Download the paper from the url with requests to the 'papers' directory.
    """
    filename = url.split('/')[-1]
    r = requests.get(url, allow_redirects=True)

    Path("papers").mkdir(parents=True, exist_ok=True)

    open(f"papers/{filename}.pdf", 'wb').write(r.content)


if __name__ == "__main__":
    app()
