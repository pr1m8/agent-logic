import nox


@nox.session(name="docs", python="3.12")
def build_docs(session: nox.Session) -> None:
    """Build the Sphinx documentation."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "docs/source",
        "docs/build/html",
    )


@nox.session(name="view-docs", python="3.12")
def view_docs(session: nox.Session) -> None:
    """Serve and auto-rebuild Sphinx documentation with live reload."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)
    session.install("sphinx-autobuild")
    session.run(
        "sphinx-autobuild",
        "docs/source",
        "docs/build/html",
        "--open-browser",
    )
