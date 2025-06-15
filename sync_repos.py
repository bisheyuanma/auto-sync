import os
import time
from github import Github

GH_PAT = os.environ.get('GH_PAT')
USER_ACCOUNT = 'xunmaw001'
OUTPUT_FILE = 'all_repos.txt'

gh = Github(GH_PAT)
user = gh.get_user(USER_ACCOUNT)

# 检查速率限制
rate_limit = gh.get_rate_limit()
remaining = rate_limit.core.remaining
reset_time = rate_limit.core.reset.timestamp()
current_time = time.time()

if remaining == 0:
    wait_seconds = reset_time - current_time + 10
    print(f"速率限制已达上限，等待 {wait_seconds} 秒...")
    time.sleep(wait_seconds)

repos = []
for repo in user.get_repos():
    repos.append(repo.full_name)
    # 每拉取 100 个检查一次速率限制
    if len(repos) % 100 == 0:
        rate_limit = gh.get_rate_limit()
        if rate_limit.core.remaining == 0:
            reset_time = rate_limit.core.reset.timestamp()
            wait_seconds = reset_time - time.time() + 10
            print(f"速率限制已达上限，等待 {wait_seconds} 秒...")
            time.sleep(wait_seconds)

with open(OUTPUT_FILE, 'w') as f:
    for full_name in repos:
        f.write(full_name + '\n')

print(f"所有仓库列表已保存到 {OUTPUT_FILE}")
