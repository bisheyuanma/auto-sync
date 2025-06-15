import os
import subprocess
from github import Github
from datetime import datetime

# 环境变量
GH_PAT = os.environ.get("GH_PAT")
BACKUP_DIR = "repo_mirrors"
SYNC_LIST_FILE = "repos_sync_list.md"

# 源账户列表（可修改或读取外部文件）
SOURCE_USERS = [
    "xunmaw001",
    "javaplay996",
    "zongjixiaoai66"
]

# 创建备份目录
os.makedirs(BACKUP_DIR, exist_ok=True)

# 初始化 Markdown 表头
if not os.path.exists(SYNC_LIST_FILE):
    with open(SYNC_LIST_FILE, "w") as f:
        f.write("| 序号 | 源仓库 | 状态 | 时间 |\n")
        f.write("| ---- | ------ | ---- | ---- |\n")

# 登录 GitHub
gh = Github(GH_PAT)

# 获取已同步的仓库集合
synced_set = set()
with open(SYNC_LIST_FILE, "r") as f:
    for line in f:
        if line.startswith("| "):
            parts = line.split("|")
            if len(parts) > 2:
                synced_set.add(parts[2].strip())

count = 0
MAX_PER_RUN = 30

for username in SOURCE_USERS:
    try:
        user = gh.get_user(username)
        repos = user.get_repos(sort="updated")
        for repo in repos:
            full_name = repo.full_name
            if full_name in synced_set:
                continue  # 跳过已同步
            status = ""
            try:
                print(f"同步中：{full_name}")
                subprocess.run([
                    "git", "clone", "--mirror",
                    f"https://x-access-token:{GH_PAT}@github.com/{full_name}.git",
                    f"{BACKUP_DIR}/{repo.name}.git"
                ], check=True)
                status = "✅ 成功"
            except subprocess.CalledProcessError:
                status = "❌ 失败或不存在"
            with open(SYNC_LIST_FILE, "a") as f:
                f.write(f"| {len(synced_set)+1} | [{full_name}](https://github.com/{full_name}) | {status} | {datetime.utcnow().isoformat()} |
")
            synced_set.add(full_name)
            count += 1
            if count >= MAX_PER_RUN:
                raise SystemExit(0)
    except Exception as e:
        print(f"跳过用户 {username}，错误：{e}")
        continue
