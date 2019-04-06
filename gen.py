import random
import json


class JobTitleMaker:
    JOBS_FILE = "data/joblines_norm.json"

    def __init__(self):
        with open(JobTitleMaker.JOBS_FILE, "r", encoding="utf-8") as ifp:
            loaded_json = json.load(ifp)
            self.joblines = loaded_json["joblines"]
            self.prefixes = loaded_json["prefix"]
            self.suffixes = loaded_json["suffix"]

    def make_response(self):
        prefix = random.choice(self.prefixes)
        suffix = random.choice(self.suffixes)
        space = random.choice((" ", ": ", " — ")) if suffix else ""
        if not any((prefix, suffix)):
            prefix = self.prefixes[0]
            suffix = "."
            space = " "
        jobline = self.make_jobline()
        return '{prefix}"{jobline}"{space}{suffix}'.format(
            prefix=prefix, jobline=jobline, space=space, suffix=suffix
        )

    def make_jobline(self):
        return random.choice(self.joblines)


jobmaker = JobTitleMaker()


def main():
    print("\n".join(jobmaker.make_message() for _ in range(10)))


if __name__ == "__main__":
    main()
