#!/bin/bash
#
#SBATCH --partition=milano
#
#SBATCH --job-name=psf_cat
#SBATCH --output=psf_catalog_output.txt
#SBATCH --error=psf_catalog_error.txt
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64g
#SBATCH --account=rubin:commissioning
#
#SBATCH --time=6:00:00


source /sdf/group/rubin/sw/w_latest/loadLSST.sh
setup lsst_distrib
setup lsst_sitcom

export DAF_BUTLER_REPOSITORY_INDEX=/sdf/group/rubin/shared/data-repos.yaml

python3 generate_psf_catalog.py