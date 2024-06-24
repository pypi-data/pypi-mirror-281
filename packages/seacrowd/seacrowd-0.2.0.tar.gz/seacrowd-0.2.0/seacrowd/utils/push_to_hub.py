import importlib
import os
import subprocess

from huggingface_hub import HfApi
from io import BytesIO

_SEA_DATASETS_PATH = "../sea_datasets/"

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def construct_readme(dsetname):
    module_path = f"seacrowd.sea_datasets.{dirname}.{dirname}"

    dset_name = import_from(module_path, "_DATASETNAME")
    description = import_from(module_path, "_DESCRIPTION")
    homepage = import_from(module_path, "_HOMEPAGE")
    is_local = import_from(module_path, "_LOCAL")
    languages = import_from(module_path, "_LANGUAGES")
    supported_tasks = import_from(module_path, "_SUPPORTED_TASKS")
    source_version = import_from(module_path, "_SOURCE_VERSION")
    seacrowd_version = import_from(module_path, "_SEACROWD_VERSION")
    citation = import_from(module_path, "_CITATION")

    readme_string = f"# {dset_name.replace("_", " ").title()}"
    readme_string += f"\n\n{description}"
    readme_string += f'''\
        \n\n## Dataset Usage
        \n\n### Load Dataset
        \n```# Load a single dataset based on the dataset name
        \nkhpos_dset = sc.load_dataset("{dset_name}", schema="seacrowd")
        \n```
    '''


if __name__ == "__main__":
    api = HfApi(
        endpoint="https://huggingface.co",
        token=os.getenv("HF_TOKEN"))
    
    init_file = BytesIO(str.encode(""))
    requirements_file = BytesIO(str.encode("seacrowd>=0.1.3"))
    
    for dirname in ["indolem_sentiment"]:
    # for dirname in os.listdir(_SEA_DATASETS_PATH):
        print(dirname)
        
        license_file = BytesIO(str.encode(
            import_from(f"seacrowd.sea_datasets.{dirname}.{dirname}", "_LICENSE")))
        

        readme_file = BytesIO(str.encode())
        
        api.upload_file(
            path_or_fileobj=license_file,
            path_in_repo="LICENSE",
            repo_id=f"SEACrowd/{dirname}",
            repo_type="dataset",
        )