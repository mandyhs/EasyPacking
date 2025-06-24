import subprocess
import sys

def run_python_script(script_path: str, args_dict: dict = None):
    """
    run_python_script("other_script.py", {
    "--name": "Alice",
    "--count": 3
    })
    """
    args = [sys.executable, script_path]

    # 把參數 dict 轉成 CLI 格式
    if args_dict:
        for key, value in args_dict.items():
            args.append(str(key))
            if value is not None:  # 支援 flag 類型參數（如 --verbose）
                args.append(str(value))
    
    print(f"[+++] execute: {' '.join(args)}")

    try:
        result = subprocess.run(args, check=True)
        print(f"[V] exit code: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"[X] failed!!  exit code {e.returncode}）")
        raise
