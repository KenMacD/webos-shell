import cmd
import json
import re
import readline
import subprocess
import sys


def _run(cmd):
    print(f"--> {cmd[-1]}")
    subprocess.run(cmd)
    print("")


def _expand_prefix(target):
    target = re.sub("^cl.", "com.lge.", target)
    target = re.sub("^cp.", "com.palm.", target)
    target = re.sub("^cw.", "com.webos.", target)
    return target


def _parse_args(args):
    target, *rest = args.split(" ", 1)
    target = _expand_prefix(target)
    json_str = rest[0] if rest else '{"subscribe":false}'

    return target, json.dumps(json.loads(json_str))


class WebosShell(cmd.Cmd):
    prompt = "(webos)? "

    def __init__(self):
        super().__init__()

        # Due to the slashes in the commands, adjust for readline:
        delims = readline.get_completer_delims()
        readline.set_completer_delims(delims.replace("/", ""))

    def do_EOF(self, args):
        sys.exit(0)

    def do_l(self, args):
        try:
            target, arg = _parse_args(args)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON")
            return

        _run(
            [
                "/usr/bin/ssh",
                "tv",
                f"luna-send-pub -n 1 -f luna://{target} '{arg}'",
            ]
        )

    def complete_l(self, text, line, benidx, endidx):
        text = _expand_prefix(text)
        return [i for i in TARGET_LIST if i.startswith(text)]


def run():
    WebosShell().cmdloop()
