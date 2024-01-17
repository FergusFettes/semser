from typing import Optional
from semanticscholar import SemanticScholar
import typer
import rich
import requests
from pathlib import Path


sch = SemanticScholar()
app = typer.Typer()


@app.command()
def search(query: str, limit: int = 10, author: Optional[str] = None):
    # Remove any newlines from the query
    query = query.replace("\n", " ")
    papers = sch.search_paper(query, limit=limit)

    select_and_print(papers, limit)


def select_and_print(papers, limit):

    limit = min(limit, len(papers))
    for i in range(limit):
        print_paper(papers[i], i)

    # Read in some values. If they are numbers, get those papers
    results = typer.prompt("Papers to retrieve (csl: 1,2,3 etc, or 'all')")
    if not results:
        return

    typer.echo(f"\nDownloading {results}")

    if results == "all":
        results = ",".join([str(i) for i in range(len(papers))])
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


@app.command()
def papers(filename: str):
    with open(filename, 'r') as f:
        papers = f.readlines()

    for name in papers:
        name = name.strip()
        if not name:
            continue
        paper(name, True)


@app.command()
def author(query: str, limit: int = 20):
    if not query.isdigit():
        author_id = search_author(query, limit=limit)
        if not author_id:
            return
    else:
        author_id = query

    author = sch.get_author(author_id)
    papers = author['papers']

    papers = sorted(papers, key=lambda x: x['citationCount'], reverse=True)
    select_and_print(papers, limit=limit)


def search_author(query: str, limit: int = 20):
    authors = sch.search_author(
        query,
        fields=["name", "hIndex", "citationCount", "paperCount", "authorId"],
        limit=limit
    )

    # Convert it to a list of dicts
    authors = [author for author in authors]

    # Sometimes it returns a long list, if so print an error message and truncate
    if len(authors) > 20:
        rich.print("[red]Too many results, truncating to 20[/red]\n")
        authors = authors[:20]

    # Sort by h-index and print
    authors = sorted(authors, key=lambda x: x['hIndex'], reverse=True)

    for i, author in enumerate(authors):
        print_author(author, i)

    # Read in some values. If they are numbers, get those papers from those authors
    index = typer.prompt("Author to retrieve (int)")
    if not index:
        return
    return authors[int(index)]['authorId']


def print_author(author, index):
    name = author['name']
    h_index = author['hIndex']
    citation_count = author['citationCount']
    paper_count = author['paperCount']
    id = author['authorId']

    rich.print(
        f"{index}: "
        f"{name}, "
        f"[green]h-index: {h_index}[/green], "
        f"citations: {citation_count}, "
        f"papers: {paper_count}, "
        f"ID: {id}"
    )


def print_paper(paper, index):
    title = paper['title']
    date = paper['publicationDate']
    authors = ", ".join([author['name'] for author in paper['authors']])

    citations = paper['citationCount']
    # This will be a color, used in the shell
    if paper['openAccessPdf']:
        open_status = "green"
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
    Path("~/semser_papers/").expanduser().mkdir(parents=True, exist_ok=True)
    filename = paper['title'].replace(" ", "_").replace("/", "_")[:40]
    path = Path(f"~/semser_papers/{filename}.pdf").expanduser()

    rich.print(
        f"[green]Downloading: {filename}.pdf[/green]\n"
        f"{paper['url']}"
    )

    # Check if the file has already been downloaded
    if path.exists():
        rich.print(f"[green]File already exists: {filename}.pdf[/green]\n")
        return

    if paper['openAccessPdf']:
        url = paper['openAccessPdf']['url']
        _download(url, path)
    elif 'ArXiv' in paper['externalIds']:
        url = f"https://arxiv.org/pdf/{paper['externalIds']['ArXiv']}.pdf"
        _download(url, path)
    elif 'DOI' in paper['externalIds']:
        rich.print(
            f"[red]No open access PDF available for\n[/red][i]{paper['title']}[/i]\n"
            f"[yellow]Try sci-hub:[/yellow]\nhttps://sci-hub.ru/{paper['externalIds']['DOI']}\n"
        )
    else:
        rich.print(
            f"[red]No open access PDF available for\n[/red][i]{paper['title']}[/i]\n"
        )


def _download(url, path):
    r = requests.get(url, allow_redirects=True)
    open(str(path), 'wb').write(r.content)


if __name__ == "__main__":
    app()
