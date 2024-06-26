import click
import json
from intellibot.api import IntelliBotAPI
from colorama import Fore, Style, init

init(autoreset=True)

intelli_bot = IntelliBotAPI()


@click.group()
def cli():
    pass


@cli.command()
@click.option("--username", prompt="Username", help="Username to connect")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password to connect",
)
def connect(username, password):
    """Connect to the intellibot."""
    response = intelli_bot.connect(username, password)
    if response.status_code == 200:
        click.echo(Fore.GREEN + "Connected successfully and credentials saved!")
    else:
        click.echo("Connection failed!")


@cli.command()
@click.argument("message", required=False)
def chat(message):
    """Chat with the intellibot."""
    click.echo(Fore.GREEN + "\t\t**** Welcome to intelligent chatbot!  ****\n\n")
    click.echo(Fore.GREEN + '\t\t**** Type "exit" to quit the chat. ****\n\n')

    if message:
        send_message(message)

    while True:
        message = click.prompt(Fore.BLUE + "You", type=str)
        if message.lower() in ["exit", "quit"]:
            click.echo(Fore.YELLOW + "\n\n \t\t\t***** Goodbye! *****\n\n")
            break
        send_message(message)


def send_message(message):
    try:
        response = intelli_bot.chat(message)
        if response.status_code == 200:
            click.echo(
                Fore.YELLOW
                + "\nintellibot: "
                + Style.RESET_ALL
                + f'{response.json().get("response")}\n'
            )
        else:
            click.echo(Fore.RED + "Failed to get a response from the bot.")
            click.echo(Fore.RED + f"Status Code: {response.status_code}")
            click.echo(Fore.RED + f"Response Content: {response.content}")
    except Exception as e:
        click.echo(str(e))


@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
def initialize(config_file):
    """Initialize the AI agent system with a JSON configuration."""
    try:
        with open(config_file, 'r') as file:
            config_data = json.load(file)

        response = intelli_bot.initialize_crew(config_data)
        
        if response.status_code == 200:
            click.echo(Fore.GREEN + "AI agent system initialized successfully!")
        else:
            click.echo(Fore.RED + "Failed to initialize the AI agent system.")
            click.echo(Fore.RED + f"Status Code: {response.status_code}")
            click.echo(Fore.RED + f"Response Content: {response.content}")
    except Exception as e:
        click.echo(Fore.RED + str(e))


@cli.command()
def projects():
    """Check available projects."""
    try:
        response = intelli_bot.get_active_projects()
        if response.status_code == 200:
            projects = response.json().get("projects", [])
            click.echo(Fore.GREEN + "Available Projects:")
            for project in projects:
                click.echo(Fore.GREEN + f" - {project}")
        else:
            click.echo(Fore.RED + "Failed to retrieve projects.")
            click.echo(Fore.RED + f"Status Code: {response.status_code}")
            click.echo(Fore.RED + f"Response Content: {response.content}")
    except Exception as e:
        click.echo(Fore.RED + str(e))


@cli.command()
@click.argument("project_name")
def execute(project_name):
    """Execute a project."""
    try:
        response = intelli_bot.execute_project(project_name)
        if response.status_code == 200:
            result = response.json()
            click.echo(Fore.GREEN + f"Response: {result['response']}")
            click.echo(Fore.GREEN + f"Date Created: {result['date_created']}")
        else:
            click.echo(Fore.RED + "Failed to execute the project.")
            click.echo(Fore.RED + f"Status Code: {response.status_code}")
            click.echo(Fore.RED + f"Response Content: {response.content}")
    except Exception as e:
        click.echo(Fore.RED + str(e))


@cli.command()
def user_details():
    """View active user details."""
    try:
        response = intelli_bot.get_active_user_details()
        if response.status_code == 200:
            user_details = response.json()
            click.echo(Fore.GREEN + "Active User Details:\n")
            click.echo(Fore.GREEN + f" - User ID: {user_details.get('id')}")
            click.echo(Fore.GREEN + f" - User NAME: {user_details.get('name')}")
            click.echo(Fore.GREEN + f" - User EMAIL: {user_details.get('email')}")
        else:
            click.echo(Fore.RED + "Failed to retrieve active user details.")
            click.echo(Fore.RED + f"Status Code: {response.status_code}")
            click.echo(Fore.RED + f"Response Content: {response.content}")
    except Exception as e:
        click.echo(Fore.RED + str(e))


if __name__ == "__main__":
    cli()
