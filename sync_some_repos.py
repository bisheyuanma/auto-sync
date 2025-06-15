import os
import subprocess

ALL_REPOS_FILE = 'all_repos.txt'
SYNCED_REPOS_FILE = 'synced_repos.txt'
CLONE_DIR = 'repo_mirrors'
BATCH_SIZE = 30

os.makedirs(CLONE_DIR, exist_ok=True)

# 读全部仓库
with open(ALL_REPOS_FILE, 'r') as f:
    all_repos = [line.strip() for line in f.readlines()]

# 读已同步仓库
if os.path.exists(SYNCED_REPOS_FILE):
    with open(SYNCED_REPOS_FILE, 'r') as f:
        synced_repos = set(line.strip() for line in f.readlines())
else:
    synced_repos = set()

# 过滤待同步仓库
to_sync = [r for r in all_repos if r not in synced_repos][:BATCH_SIZE]

for repo_full_name in to_sync:
    print(f"同步中：{repo_full_name}")
    clone_path = os.path.join(CLONE_DIR, repo_full_name.replace('/', '__'))
    git_url = f'https://github.com/{repo_full_name}.git'
    
    if os.path.exists(clone_path):
        # 已有镜像，拉取更新
        cmd = ['git', '--git-dir', clone_path, 'remote', 'update']
    else:
        # 还没克隆，做镜像克隆
        cmd = ['git', 'clone', '--mirror', git_url, clone_path]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"同步成功：{repo_full_name}")
        # 记录已同步
        with open(SYNCED_REPOS_FILE, 'a') as f:
            f.write(repo_full_name + '\n')
    else:
        print(f"同步失败：{repo_full_name}，错误信息：{result.stderr}")

print("本批同步完成。")
