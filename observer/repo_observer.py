"""
Check for new commits to the master repo and notifies dispatcher of the
latest commit id so that the dispatcher can dispatch the tests against
this commit id
"""
import argparse
import helpers
import os
import socket
import subprocess
import time


def poll():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatcher-server",
                        help="dispatcher host:port, "\
                        "by default it uses localhost:8888",
                        default="localhost:8888",
                        action="store")
    parser.add_argument("repo", metavar="REPO", type=str,
                        help="path to the repository to observe")
    args = parser.parse_args()
    dispatcher_host, dispatcher_port = args.dispatcher_server.split(":")

    while True:
        try:
            # call the bash script to update the repo and check
            # for changes.
            subprocess.check_output(["../scripts/update_repo.sh", args.repo])
        except subprocess.CalledProcessError as e:
            raise Exception(f"Could not update and check repository. Reason: "
                            f"{e.output}")

        if os.path.isfile("../scripts/.commit_id"):
            # Check dispatcher's status to confirm that we can send tests
            try:
                response = helpers.communicate(dispatcher_host,
                                               int(dispatcher_port),
                                               "status")
            except socket.error as error:
                raise Exception(f"Could not communicate with dispatcher "
                                f"server: {error}")

            if response == "OK":
                # found a dispatcher, let's send a test
                commit = ""
                with open("../scripts/.commit_id", "r") as f:
                    commit = f.readline()
                response = helpers.communicate(dispatcher_port,
                                               int(dispatcher_host),
                                               f"dispatch: {commit}")
                if response != "OK":
                    raise Exception(f"Could not dispatch the test: {response}")
                print("dispatched")
            else:
                raise Exception(f"Could not dispatch the test: {response}")
        time.sleep(5)
