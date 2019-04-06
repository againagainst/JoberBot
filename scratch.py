import json
import os
import re
from pprint import pprint

import pymorphy2

job = re.compile(r"│\d* +│ +\d* +│(.*)│")


def main():
    dump_joblines(read_json_joblines("joblines_010_93_data.json"),  "joblines_norm.json")
    # dump_joblines(joblines("ok_010_93.txt"),  "joblines.json")
    # dump_joblines(morfy_joblines(set(joblines("ok_010_93.txt"))), "joblines_norm.json")


def read_json_joblines(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        for job in data:
            jobline = job.get('NAME')
            if jobline:
                yield jobline


def morfy_joblines(iterlines):
    morph = pymorphy2.MorphAnalyzer()
    for jobline in iterlines:
        if ' ' in jobline:
            yield jobline
        else:
            parsed = morph.parse(jobline)[0]
            yield parsed.normal_form.capitalize()


def dump_joblines(iterlines, outname):
    with open(outname, "w", encoding="utf-8") as ofp:
        json.dump({"joblines": list(iterlines)}, ofp, ensure_ascii=False, indent=4)
    print("Done")


def stripe_job(jobline: str) -> str:
    space_removed_jobline = " ".join(jobline.split())
    return space_removed_jobline.strip().capitalize()


def joblines(filename):
    with open(filename, encoding="utf-8") as fp:
        job_line_iter = iter(job.findall(fp.read()))
        newjob_line = next(job_line_iter)
        jobline = ""
        for chunk in job_line_iter:
            if chunk == newjob_line:
                jobline = stripe_job(jobline)
                if jobline and len(jobline) < 200:
                    yield jobline
                    jobline = ""
                continue
            jobline = jobline + chunk


if __name__ == "__main__":
    main()
