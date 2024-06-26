import click
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

from hawk_tui.db_connectors import postgresql, mysql, kafka, redis, elasticsearch

class DBConnectorApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="content")
        yield Footer()

    def update_content(self, content: str):
        self.query_one("#content", Static).update(content)

@click.group()
def hawk():
    pass

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def postgresql(host, port, username, password, database):
    '''
    
    '''
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def mysql(host, port, username, password, database):
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def kafka(host, port, username, password, database):
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def redis(host, port, username, password, database):
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def elasticsearch(host, port, username, password, database):
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

# Similar commands for other databases...

if __name__ == '__main__':
    hawk()