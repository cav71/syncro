import sys
import time
import shlex
import functools
import inspect


class RemoteExecError(Exception):
    pass


def remote(transport, cmd, abort=True, poll_s=0.1):
    session = transport.open_session()
    if not isinstance(cmd, str):
        cmd = shlex.join(cmd).replace("'", '"')
    session.exec_command(cmd)

    while not session.exit_status_ready():
        time.sleep(poll_s)

    err = ""
    while buf := session.recv_stderr(100):
        err += str(buf, encoding="utf-8")
    
    out = ""
    while buf := session.recv(100):
        out += str(buf, encoding="utf-8")
    status = session.recv_exit_status()
    if abort and status:
        raise RemoteExecError("command failed", cmd, status, err) 
    return status, out, err


def shell(transport):
    channel = transport.open_session()

    channel.invoke_shell()

    stdin = channel.makefile("wb")
    stdout = channel.makefile("r")

    #indata = os.fdopen(sys.stdin.fileno(), 'r', 1)
    ask = input("> ")
    stdin.write(ask)
    stdin.flush()
    print("Got")
    for line in stdout:
        print(line)
    
    
