import os
import shutil

def copy_validate_api_key():
    src = os.path.join(os.path.dirname(__file__), 'validate_api_key.py')
    dst = os.path.join(os.getcwd(), 'validate_api_key.py')
    
    if os.path.abspath(src) != os.path.abspath(dst):
        if os.path.exists(src):
            shutil.copyfile(src, dst)
            print(f"Copied {src} to {dst}")
        else:
            print(f"Source file {src} not found at {src}")
    else:
        print(f"Source and destination are the same. No need to copy.")

if __name__ == "__main__":
    copy_validate_api_key()
