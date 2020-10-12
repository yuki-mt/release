from metaflow import Flow, Run, Metaflow
import subprocess
from typing import Optional


def get_run(flow_id: str,
            param: dict = {},
            script_path: Optional[str] = None,
            overwrite: bool = False) -> Run:
    flow_ids = [f.id for f in Metaflow().flows]
    if flow_id in flow_ids and not overwrite:
        flow = Flow(flow_id)
        for run in flow:
            if not run.successful:
                continue
            run_data = run.data.__dict__['_artifacts']
            if all(k in run_data and run_data[k].data == v for k, v in param.items()):
                return run
    if script_path is None:
        raise ValueError('No run was found')

    argument = ' '.join(f'--{k} {v}' for k, v in param.items())
    subprocess.run(f"python {script_path} run {argument}", shell=True)

    run = Flow(flow_id).latest_run
    if run.successful:
        return run
    else:
        raise ValueError('The new run failed')
