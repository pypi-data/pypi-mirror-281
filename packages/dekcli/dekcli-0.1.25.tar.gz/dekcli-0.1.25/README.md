### dekcli

#### 1. gitea
```shell
# Input a token from gitea website, the token has all permissions.
dekcli gitea login https://xx.gitearepos.site --username xxxx

# git-set's repo dir path format: git-set/org/repo/.git
dekcli gitea init /path/to/git-set

# change some orgs to public

# Add local ssh token to the gitea website settings, then clone a mirror repo to add .ssh/known_hosts

# Add gitea runner to cluster

dekcli gitea push /path/to/git-set
dekcli gitea pull /path/to/git-set
```
