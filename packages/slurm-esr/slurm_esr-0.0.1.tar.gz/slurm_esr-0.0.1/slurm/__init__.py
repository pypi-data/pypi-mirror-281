HEAD_INFO = """#!/bin/bash
#SBATCH --job-name {job_name}
#SBATCH --partition {partition}
#SBATCH --output {workdir}/log/{job_name}.%A.%a.out # STDOUT
#SBATCH --error {workdir}/log/{job_name}.%A.%a.log # STDERR
"""
