# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/3

import toml
import subprocess

conf_name = "./pyproject.toml"

# 读取 toml 文件
with open(conf_name, "r") as f:
    config = toml.load(f)

# 获取git版本
command1 = ['git', 'describe', '--tags', '--always']
command2 = ['sed', 's/-g.*$//']
result1 = subprocess.run(command1, stdout=subprocess.PIPE, check=True, encoding='utf-8')
result2 = subprocess.run(command2, input=result1.stdout, stdout=subprocess.PIPE, check=True, encoding='utf-8')
git_version = result2.stdout.strip()
print(git_version)


# 修改属性值
config['tool']['poetry']['version'] = git_version

# 写回 toml 文件
with open(conf_name, "w") as f:
    toml.dump(config, f)

