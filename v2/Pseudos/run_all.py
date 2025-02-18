import os

def find_and_run_scripts(base_dir):
    for root, _, files in os.walk(base_dir):
        depth = root[len(base_dir):].count(os.sep)
        if 1 <= depth:
            for file in files:
                if file.endswith(".py"):
                    script_path = os.path.join(root, file)
                    os.chdir(root)
                    nohup_path = os.path.join(root, "nohup.out")
                    if os.path.exists(nohup_path):
                        os.remove(nohup_path)

                    os.system(f"nohup python3 {script_path} -op -maxiter 1700 &")
                    os.chdir(base_dir)

if __name__ == "__main__":
    base_directory = os.getcwd()
    find_and_run_scripts(base_directory)

