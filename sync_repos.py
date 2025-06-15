import os
from github import Github

GH_PAT = os.environ.get('GH_PAT')
USER_ACCOUNT = 'xunmaw001'
OUTPUT_FILE = 'all_repos.txt'

gh = Github(GH_PAT)
user = gh.get_user(USER_ACCOUNT)

repo = next(user.get_repos(), None)

with open(OUTPUT_FILE, 'w') as f:
    if repo:
        f.write(repo.full_name + '\n')
        print(f"仓库 {repo.full_name} 已保存到 {OUTPUT_FILE}")
    else:
        print("该用户没有公开仓库")
