# sync_repos.py

import os
import re
import subprocess
import time
from datetime import datetime
from github import Github

# 读取环境变量
GITHUB_TOKEN = os.getenv("GH_PAT")
GITHUB_USERNAME = os.getenv("GITHUB_ACTOR")
MARKDOWN_FILE = "repos_sync_list.md"
MAX_SYNC = 1  # 测试阶段先同步 1 个

# 初始化 GitHub API
gh = Github(GITHUB_TOKEN)
user = gh.get_user()

def parse_markdown_table(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    rows = []
    for line in lines:
        if line.strip().startswith('|') and not line.strip().startswith('| 序号') and not line.strip().startswith('| ----'):
            parts = [part.strip() for part in line.strip().split('|')[1:-1]]
            rows.append(parts)
    return rows, lines

def write_markdown_table(lines, updated_rows):
    with open(MARKDOWN_FILE, 'w', encoding='utf-8') as f:
        for i, line in enumerate(lines):
            if i < 3:
                f.write(line)
            else:
                index = i - 3
                if index < len(updated_rows):
                    row = updated_rows[index]
                    new_line = '| ' + ' | '.join(row) + ' |\n'
                    f.write(new_line)

def sync_repo(source_owner, repo_name):
    src_url = f"https://github.com/{source_owner}/{repo_name}.git"
    dest_repo_name = f"{source_owner}-{repo_name}"

    # 1. clone
    subprocess.run(["git", "clone", "--mirror", src_url], check=True)
    os.chdir(f"{repo_name}.git")

    # 2. create target repo via API
    new_repo = user.create_repo(dest_repo_name, private=False, auto_init=False)
    dest_url = new_repo.clone_url.replace("https://", f"https://{GITHUB_TOKEN}@")

    # 3. push to new repo
    subprocess.run(["git", "push", "--mirror", dest_url], check=True)
    os.chdir("..")
    subprocess.run(["rm", "-rf", f"{repo_name}.git"])

    return new_repo.html_url

def main():
    rows, lines = parse_markdown_table(MARKDOWN_FILE)
    synced = 0

    for row in rows:
        if row[4].upper() != "TRUE":
            source_owner = row[1]
            repo_name = row[2]

            try:
                print(f"同步中：{source_owner}/{repo_name}")
                new_url = sync_repo(source_owner, repo_name)
                row[4] = "TRUE"
                row[5] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                row[6] = new_url
                synced += 1
            except Exception as e:
                print(f"同步失败：{source_owner}/{repo_name}，错误：{e}")

            if synced >= MAX_SYNC:
                break

    write_markdown_table(lines, rows)

if __name__ == '__main__':
    main()
