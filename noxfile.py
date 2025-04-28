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


@nox.session(name="docs-autobuild", python="3.12")
def autobuild_docs(session: nox.Session) -> None:
    """Auto-rebuild Sphinx docs on file changes."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)
    session.run(
        "sphinx-autobuild",
        "docs/source",
        "docs/build/html",
    )
