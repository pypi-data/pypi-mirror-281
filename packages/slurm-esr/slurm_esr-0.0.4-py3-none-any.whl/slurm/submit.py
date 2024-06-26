from os import makedirs
from os.path import exists, join
from subprocess import run
from uuid import uuid4

from slurm import HEAD_INFO, PRIORITY


def write_job_list(job_list: list, workdir: str) -> str:
    """Write job list into a file

    Args:
        job_list (list): Job list, e.g., [cmd1, cmd2, cmd3, ...]
        workdir (str): Working directory

    Returns:
        str: the file contains job list
    """
    my_list = [item + "\n" for item in job_list]
    job_list_file = join(workdir, "cmdlist.txt")
    with open(job_list_file, "w") as f:
        for line in my_list:
            f.write(line)

    return job_list_file


def write_sl(
    job_name: str,
    partition: str,
    memory_per_node: int or None,
    python_path: str or None,
    conda_env: str or None,
    job_priority: str,
    workdir: str,
) -> str:
    """Write slurm sl file

    Args:
        job_name (str): Job name
        partition (str): prod or dev
        memory_per_node (intorNone): Memory per node (e.g., 4000)
        python_path (strorNone): Python path to be used
        conda_env (strorNone): Conda env to be used
        workdir (str): Working directory

    Returns:
        str: sl file path
    """
    header = HEAD_INFO.format(
        job_name=job_name,
        partition=partition,
        workdir=workdir,
        nice_value=PRIORITY[job_priority],
    )

    if memory_per_node is not None:
        header += f"#SBATCH --mem={memory_per_node}"

    sl_contents = [header]

    if python_path is not None:
        sl_contents.append(f"export PYTHONPATH={python_path}")

    if conda_env is not None:
        sl_contents.append(f"source activate {conda_env}")

    sl_contents.append('COMMAND=`sed "${SLURM_ARRAY_TASK_ID}q;d" ${CMDS_LIST}`')
    sl_contents.append("echo $COMMAND")
    sl_contents.append("eval $COMMAND")

    my_list = [item + "\n" for item in sl_contents]
    jobarray_file = join(workdir, "jobarray.sl")
    with open(jobarray_file, "w") as f:
        for line in my_list:
            f.write(line)

    return jobarray_file


def submit(
    job_name: str,
    job_list: list,
    python_path: str or None = None,
    conda_env: str or None = None,
    total_jobs: int or None = 3,
    memory_per_node: int or None = 4000,
    job_priority: str = "default",
    partition: str = "prod",
    workdir: str or None = None,
    debug: bool = False,
):

    if job_priority not in ["default", "low", "high"]:
        raise Exception("Job priority must be chosen from [default, low, high]")

    if partition not in ["prod", "dev"]:
        raise Exception("Partition must be chosen from [prod, dev]")

    if workdir is None:
        workdir = f"slurm_{job_name}_{uuid4()}"

    workdir_log = join(workdir, "log")

    if not exists(workdir_log):
        makedirs(workdir_log)

    job_list_file = write_job_list(job_list, workdir)
    sl_file = write_sl(
        job_name,
        partition,
        memory_per_node,
        python_path,
        conda_env,
        job_priority,
        workdir,
    )

    num_jobs = sum(1 for line in open(job_list_file))

    submit_job = [
        "sbatch",
        "--array=1-" + str(num_jobs) + ("" if total_jobs is None else f"%{total_jobs}"),
        "--export=ALL,CMDS_LIST=" + job_list_file,
        sl_file,
    ]

    print(" ".join(submit_job))

    if not debug:
        run(submit_job)
