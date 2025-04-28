import nox

@nox.session(name="docs", python="3.12")
def build_docs(session: nox.Session) -> None:
    """Build the Sphinx documentation."""
    # Install the 'docs' extras group
    session.run("poetry", "install", "--with", "docs", external=True)

    # Change directory into docs/ if you have it (optional)
    # session.chdir("docs")   # <-- uncomment if you have a separate /docs/ folder

    # Actually build the docs
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")
