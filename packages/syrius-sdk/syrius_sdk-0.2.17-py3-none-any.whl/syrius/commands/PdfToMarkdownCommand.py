from syrius.commands.abstract import Command, AbstractCommand


class PdfToMarkdownCommand(Command):
    """ """
    id: int = 33
    filename: str | AbstractCommand
