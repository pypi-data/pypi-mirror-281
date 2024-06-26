import json
import pprint

from loader.load import load_job_configuration

from src.exporter.export import export_jobs_yml


def adhoc():
    with open("tests/loader/jobs_with_anchors.yml") as file:
        loaded_config = load_job_configuration(file, None)
        # print(loaded_config.model_dump_json())
        # pprint.pprint(loaded_config.model_dump())

        jobs = [v for k, v in loaded_config.jobs.items()]
        export_jobs_yml(jobs)


if __name__ == "__main__":
    adhoc()
