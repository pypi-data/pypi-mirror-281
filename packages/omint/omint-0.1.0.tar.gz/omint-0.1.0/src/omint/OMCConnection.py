import random
import shutil
import subprocess

import zmq


class OMCConnection:

    def __init__(self, random_socket_name=False, port=10000):
        self._omc_process = self._start_omc_process(random_socket_name, port)
        self._context = zmq.Context()
        self._omc_socket = self._context.socket(zmq.REQ)
        self._omc_socket.connect(f"tcp://localhost:{port}")

    def __del__(self):
        self._omc_process.terminate()

    def _start_omc_process(self, random_socket_name, port):
        rand_string = str(random.randbytes(8))
        omc_executable = shutil.which("omc")
        cmd = [
            omc_executable, "--interactive=zmq", f"--interactivePort={port}"
        ]
        if random_socket_name:
            cmd.append(f"-z={rand_string}")

        proc = subprocess.Popen(cmd)

        return proc

    def send(self, expression):
        self._omc_socket.send_string(expression)

        return self._omc_socket.recv_string()
