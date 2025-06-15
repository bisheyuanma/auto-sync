import os
from github import Github

GH_PAT = os.environ.get('GH_PAT')
USER_ACCOUNT = 'xunmaw001'
OUTPUT_FILE = 'all_repos.txt'

gh = Github(GH_PAT)
user = gh.get_user(USER_ACCOUNT)
repos = user.get_repos()

with open(OUTPUT_FILE, 'w') as f:
    for repo in repos:
        f.write(f'{repo.full_name}\n')

print(f'所有仓库列表已保存到 {OUTPUT_FILE}')
