import argparse

from sudogpt import SudoGPT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        help="a natural language expression of a cli-based task you want sudogpt to accomplish",
        required=True,
    )
    parser.add_argument(
        "--use-helper",
        help="employ a second assistant to give advice to the first",
        action="store_true"
    )
    parser.add_argument(
        "--skip-approval",
        help="run scripts without approving them (dangerous!)",
        action="store_true",
    )

    args = parser.parse_args()

    approve = not args.skip_approval
    s = SudoGPT(args.task, approve, args.use_helper)
    s.go()
