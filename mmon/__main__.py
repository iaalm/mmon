import argparse
import atexit
import logging
import sys
from os import environ, path
from typing import Optional

from loguru import logger

from mmon.__about__ import __version__
from mmon.config import load_config
from mmon.engine import Engine


def setup_readline():
    try:
        import readline
    except ImportError:
        logger.warning(
            "Module readline not available. Please install 'readline' or 'pyreadline'."
        )
        return

    histfile = path.join(path.expanduser("~"), ".mmon_history")
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)


def get_input() -> Optional[str]:
    try:
        return input("> ")
    except EOFError:
        return None


def main():
    parser = argparse.ArgumentParser(description="mmon v" + __version__)
    parser.add_argument(
        "question",
        default="",
        nargs="?",
        type=str,
        help="Initial prompt to start the conversation.",
    )
    parser.add_argument("-v", action="count", default=0, help="verbose level")
    parser.add_argument(
        "--gen_cfg",
        action="store_true",
        help="Regenerate config from environment variables.",
    )
    args = parser.parse_args()

    logger.remove()
    log_format = "{message}"
    if args.v >= 2:
        logger.add(sys.stderr, level="DEBUG", format=log_format)
    elif args.v >= 1:
        logger.add(sys.stderr, level="INFO", format=log_format)
    else:
        logger.add(sys.stderr, level="WARNING", format=log_format)

    if args.v < 3:
        # avoid "WARNING! deployment_id is not default parameter."
        langchain_logger = logging.getLogger("langchain.chat_models.openai")
        langchain_logger.disabled = True

    load_config(gen_cfg=args.gen_cfg)
    setup_readline()
    engine = Engine(verbose_level=args.v)
    p = args.question or get_input()
    while p is not None:
        if len(p) > 0:
            response = engine.run(p)
            print(response + "\n")
        p = get_input()


if __name__ == "__main__":
    main()
