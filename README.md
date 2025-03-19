## Magnezone
Magnezone is a repo merger for the output from [Spinarak](https://github.com/fortheusers/spinarak) (managed at [switch-hbas-repo](https://github.com/fortheusers/switch-hbas-repo/tree/main)) and [Dragonite](https://github.com/fortheusers/dragonite) (managed over Discord).

It exists to allow both external contributions via Github but continue allowing the existing repo to function via manual FTP uploads.

### How to use
Specify REPO1 and REPO2 at the top of `magnezone.py`, then run with no arguments. It will automatically download each repo, and merge the contents, ignoring duplicate entries from REPO2:
```
python3 magnezone.py
```

repo1.json and repo2.json must be manually deleted to have their packages refreshed.

### TODO
- Allow deleting these via a command line argument, which a Github/Discord hook will hit
- Clear CDN using environment variables
- Nginx reverse_proxy to both repos, for serving package assets/zips from both
- Dockerize

### Diagram
<img width="1424" alt="Screenshot 2025-03-19 at 12 23 15 AM" src="https://github.com/user-attachments/assets/310a5c32-b3a8-4889-bca9-0364a6f1d1d7" />

### License
MIT!
