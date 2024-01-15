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
        print_paper(papers[i], i)

    # Read in some values. If they are numbers, get those papers
    results = typer.prompt("Papers to retrieve (csl: 1,2,3 etc)")
    if not results:
        return

    typer.echo(f"\nDownloading {results}")

    if results == "all":
        results = ",".join([str(i) for i in range(limit)])
    for result in results.split(','):
        download(papers[int(result)])


@app.command()
def paper(paper: str, y: bool = False):
    if "www.semanticscholar" in paper:
        id = paper.split("/")[-1]
    else:
        id = paper

    paper = sch.get_paper(id)
    print_paper(paper, 0)

    if not y:
        y = typer.confirm("Retrieve paper?", abort=True)
    if y:
        download(paper)


def print_paper(paper, index):
    title = paper['title']
    date = paper['publicationDate']
    authors = ", ".join([author['name'] for author in paper['authors']])

    citations = paper['citationCount']
    # This will be a color, used in the shell
    if paper['openAccessPdf']:
        open_status = paper['openAccessPdf']['status'].lower()
        open_status = "green" if open_status in ["green", "gold", "hybrid"] else "red"
    else:
        open_status = "red"
    rich.print(
        f"{index}: "
        f"{date}, "
        f"[{open_status}]({citations})[/{open_status}] "
        f"{title}, "
        f"[i]{authors}[/i]"
    )


def download(paper):
    """
    Download the paper from the url with requests to the 'papers' directory.
    """
    if paper['openAccessPdf']:
        url = paper['openAccessPdf']['url']
    else:
        typer.echo(f"No open access PDF available for {paper['title']}")
        return
    r = requests.get(url, allow_redirects=True)

    Path("papers").mkdir(parents=True, exist_ok=True)
    filename = paper['title'].replace(" ", "_")[:40]

    open(f"papers/{filename}.pdf", 'wb').write(r.content)


if __name__ == "__main__":
    app()
