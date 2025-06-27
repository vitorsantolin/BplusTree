from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from commands import VirtualFileSystem


class BPlusTreeShell(App):
    """Interface de linha de comando simulando um sistema de arquivos baseado em árvore B+."""

    CSS = """
    #header {
        background: #2e3440;
        color: #88c0d0;
        padding: 1;
        text-align: center;
        border-bottom: solid gray;
    }

    #output {
        background: #3b4252;
        color: #d8dee9;
        border: solid gray;
        height: 80%;
        overflow-y: auto;
        padding: 1;
    }

    #input {
        background: #2e3440;
        color: #eceff4;
        border-top: solid gray;
        height: 3;
    }

    #cwd {
        background: #242933;
        color: lightgreen;
        padding: 1;
        border-top: solid gray;
    }
    """



    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Static("Terminal", id="header")
        yield Static("", id="output", expand=True)
        yield Input(placeholder="Escreva um comando: ", id="input")
        yield Static("CWD: /", id="cwd")

    def on_mount(self):
        self.vfs = VirtualFileSystem()
        self.output = self.query_one("#output", Static)
        self.input = self.query_one("#input", Input)
        self.cwd_legenda = self.query_one("#cwd", Static)
        self.sair = False
        self.prompt()

    def prompt(self, text: str = ""):
        """Exibe o prompt com o caminho atual."""
        self.output.update(f"{self.vfs.cwd}$ {text}")

    def process_command(self, cmd: str) -> str:
        """Processa o comando digitado pelo usuário."""
        args = cmd.strip().split()
        if not args:
            return ""

        op, *params = args

        match op:
            case "mkdir" if params:
                return self.vfs.mkdir(params[0])
            case "ls":
                return self.vfs.ls(params[0] if params else None)
            case "cd" if params:
                return self.vfs.cd(params[0])
            case "touch" if params:
                return self.vfs.touch(params[0])
            case "rm" if params:
                return self.vfs.rm(params[0])
            case "sair":
                self.sair = True
                return ""
            case _:
                return f"Comando desconhecido ou incompleto: {cmd}"

    async def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value.strip()
        output = self.process_command(cmd)

        if self.sair:
            await self.action_quit()
            return

        self.output.update(f"{self.vfs.cwd}$ {cmd}\n{output}")
        self.cwd_legenda.update(f"CWD: {self.vfs.cwd}")
        self.input.value = ""


if __name__ == "__main__":
    BPlusTreeShell().run()
