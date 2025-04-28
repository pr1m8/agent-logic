import nox

@nox.session(name="docs", python="3.12")
def build_docs(session: nox.Session) -> None:
    session.run("poetry", "install", "--with", "docs", external=True)
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/build/html")
