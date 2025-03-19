## Magnezone
Magnezone is a repo merger for the output from [Spinarak](https://github.com/fortheusers/spinarak) (managed at [switch-hbas-repo](https://github.com/fortheusers/switch-hbas-repo/tree/main)) and [Dragonite](https://github.com/fortheusers/dragonite) (managed over Discord).

It exists to allow both external contributions via Github but continue allowing the existing repo to function via manual FTP uploads.

### How to use
Specify REPO1 and REPO2 at the top of `magnezone.py`, then run with no arguments. It will automatically download each repo, and merge the contents, ignoring duplicate entries from REPO2:
```
python3 magnezone.py
```

To run the server instead:
```
python3 magnezone.py serve
```

Which has two endpoints, `/refresh` and `/repo.json`. The former can be called with a parameter `repo` which can be `repo1` or `repo2`, to only refresh that half of the merged repo.

### TODO
- Allow deleting cached repo JSON via a Github/Discord hook will hit
- Clear CDN using environment variables
- Dockerize Nginx setup

### Diagram
<img width="1424" alt="Screenshot 2025-03-19 at 12 23 15 AM" src="https://github.com/user-attachments/assets/310a5c32-b3a8-4889-bca9-0364a6f1d1d7" />

Specifically, using the example `nginx.conf`, we have the following setup:

- Merged: `https://merged-switch-repo.b-cdn.net` (CDN for `https://magnezone.fortheusers.org`)
    - Primary: `switch-hbas-repo.b-cdn.net` (CDN for [switch-hbas-repo](https://github.com/fortheusers/switch-hbas-repo))
    - Secondary: `https://hbas-switch.b-cdn.net` (CDN for `https://switchbru.com/appstore`)

And then the `switch.cdn.fortheusers.org` domain is pointed to the merged repo CDN address, which is ultimately what is presented to both the console and web HBAS clients.

For more info on that endpoint, see [hb-app.store/api-info](https://hb-app.store/api-info).

### License
MIT!
