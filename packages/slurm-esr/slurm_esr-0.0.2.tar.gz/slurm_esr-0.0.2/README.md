# Slurm_ESR

This is a streamlined interface designed to facilitate the submission of jobs via Slurm, tailored specifically for the ESR on-premise High Performance Computing (HPC) system.

# Install
The package can be installed via:
```
pip install slurm_esr
```


# Usage
### A simple example:
Submit a job with the name ``test``, and the list of commands of ``cmd1`` and ``cmd2``.
```
from slurm.submit import submit
submit(job_name="test", job_list=["cmd1", "cmd2"])
```

The arguments of ``job_name`` and ``job_list`` are the minimum that we need to have.

### A full example:


```
from slurm.submit import submit
submit(
    job_name="test",
    job_list=["cmd1", "cmd2"],
    python_path="/tmp/test",
    conda_env="test_conda",
    total_jobs=3,
    memory_per_node=4000,
    job_priority="default",
    partition="prod",
    workdir="/tmp/test_slurm",
    debug=True
)
```

- ``job_name="test"``: This is the name of the job that you are submitting. It’s a string and in this case, the job name is ``test``.
- ``job_list=["cmd1", "cmd2"]``: This is a list of commands that you want to run as part of the job. Each command is a string. In this case, there are two commands: ``cmd1`` and ``cmd2``.
- ``python_path="/tmp/test"``: This is the path to the Python environment where the job will be run. It’s a string and in this case, the path is ``/tmp/test``. This argument is particularly useful before the code deployment/packaging.
- ``conda_env="test_conda"``: This is the name of the conda environment where the job will be run. It’s a string and in this case, the environment name is ``test_conda``.
- ``total_jobs=3``: This is the total number of jobs that you want to submit. It’s an integer and in this case, the total number of jobs is 3.
- ``memory_per_node=4000``: This is the amount of memory (in MB) that you want to allocate for each node. It’s an integer and in this case, the memory per node is 4000 MB.
- ``job_priority="default"``: This is the priority of the job. It’s a string and in this case, the job priority is ``default``. [Must chosen from default, low, high].
- ``partition="prod"``: This is the partition where the job will be run. It’s a string and in this case, the partition is ``prod``. [Must chosen from prod, dev]
- ``workdir="/tmp/test_slurm"``: This is the working directory for the job. It’s a string and in this case, the working directory is ``/tmp/test_slurm``. If this is not set, an working directory with unique ID will be automatically created.
- ``debug=True``: when set it to True, no actual job will be submitted

