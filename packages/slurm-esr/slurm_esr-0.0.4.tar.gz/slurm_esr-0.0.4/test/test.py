from slurm.submit import submit

# submit(job_name="test", job_list=["cmd1", "cmd2"])


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
    debug=True,
)
