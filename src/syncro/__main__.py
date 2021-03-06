"""starts a sync remote server
"""
import os
import getpass
import pathlib
import logging

import click
from . import cli

import paramiko
import paramiko.sftp_client

import syncro.support as support
import syncro.cli as cli


logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument("host")

    parser.add_argument("-u", "--username", default=getpass.getuser())
    parser.add_argument("-p", "--password")


def process_options(options):
    pass


def main(options):
    host, port, username = options.host, 22, options.username
    startup_delay_s = 2




    print(support.remote(transport, ["ls", "-la",])[1])
    #print(support.remote(transport, ["/bin/echo", "$$",]))
    #print(support.remote(transport, ["/bin/echo", "$$",]))

    sftp = paramiko.sftp_client.SFTPClient.from_transport(transport)

    # transfer the remote server
    sftp.put(pathlib.Path(__file__).parent / "remote.py", "remote.py")

    # connect the secure end points
    support.shell(transport)


@click.command()
@click.argument("host")
@click.option('--password', hide_input=True)
@click.option('--username', default=lambda: getpass.getuser())
@cli.standard(quiet=True)
def main(host, username, password):
    "hello world"
    logger.debug("A")
    logger.info("B")
    logger.warning("C")
    port = 22
    print("one", username, password)
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.load_host_keys(pathlib.Path("~/.ssh/known_hosts").expanduser())
    client.connect(host, port, username=username, password=password)

    transport = client.get_transport()
    transport.set_keepalive(2)

    print(support.remote(transport, ["ls", "-la",])[1])

# @cli.add_logging()
# def two(*args, **kwargs):
#     print("two", args, kwargs)
#
# @cli.add_logging(1, b=2)
# def three(*args, **kwargs):
#     print("three", args, kwargs)

if __name__ == '__main__':
    main()
