#!/usr/bin/env python
import os
import sys
import subprocess

def main():
    # 获取安装的fastp路径
    # /cluster/home/Kangwen/anaconda3/envs/stark/lib/python3.9/site-packages/sc3dg/fastp/bin/fastp
    # /cluster/home/Kangwen/Hic/AAA_tutorial/sc3dg/sc3dg/fastp
    fastp_path = os.path.join(os.path.dirname(__file__), 'fastp')
    
    if not os.path.exists(fastp_path):
        print(f"Error: Samtools executable not found at {fastp_path}", file=sys.stderr)
        sys.exit(1)
    
    # 构建完整的命令，包括所有参数
    command = [fastp_path] + sys.argv[1:]
    
    try:
        # 执行fastp命令
        # chmod u+x
        subprocess.run(["chmod", "u+x", fastp_path], check=True)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing fastp: {e}", file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()