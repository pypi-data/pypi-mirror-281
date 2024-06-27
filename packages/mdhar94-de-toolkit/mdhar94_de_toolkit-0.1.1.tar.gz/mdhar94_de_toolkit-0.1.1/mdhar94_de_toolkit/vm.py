import click
import subprocess

@click.command()
def start():
    """
        Start your vm
    """
    subprocess.run(['gcloud', 'compute', 'instances', 'start'
                    , '--zone=europe-west1-b', 'lewagon-data-eng-vm-mdhar94'])

@click.command()
def stop():
    """
        Stop your vm
    """
    subprocess.run(['gcloud', 'compute', 'instances', 'stop'
                    , '--zone=europe-west1-b', 'lewagon-data-eng-vm-mdhar94'])

@click.command()
def connect():
    """
        Connect to your vm in vscode inside your ~/code/MDhar94/folder
    """
    subprocess.run(['code', '--folder-uri'
                   ,'vscode-remote://ssh-remote+mischadhar94@34.77.124.8/home/mischadhar94/code/MDhar94'])
