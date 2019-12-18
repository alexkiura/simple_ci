"""
Check for new commits to the master repo and notifies dispatcher of the
latest commit id so that the dispatcher can dispatch the tests against
this commit id
"""
import argparse
import helpers
import subprocess


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

