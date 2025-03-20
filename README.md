## Magnezone
Magnezone is a repo merger for the output from [Spinarak](https://github.com/fortheusers/spinarak) (managed at [switch-hbas-repo](https://github.com/fortheusers/switch-hbas-repo/tree/main)) and [Dragonite](https://github.com/fortheusers/dragonite) (managed over Discord).

It exists to allow both external contributions via Github but continue allowing the existing repo to function via manual FTP uploads.

### How to use
Specify primary and secondary repo URLs in `config.json`, then run the python script no arguments. It will automatically download each repo, and merge the contents, ignoring duplicate entries from the secondary:
```
python3 magnezone.py
```

To run the server instead:
```
python3 magnezone.py serve
```

Which has two endpoints, `/refresh` and `/repo.json`. The former can be called with a parameter `repo` which can be `primary` or `secondary`, to only refresh that half of the merged repo.

The refresh endpoint also accepts a list of packages separated by comma, to match the output that Spinarak provides in CI mode. If provided, it will clear those package URLs on the upstream (primary/secondary) repo, refresh/merge, and then clear them again from the merged repo URL.

### Diagram
<img width="1424" alt="Screenshot 2025-03-19 at 12 23 15 AM" src="https://github.com/user-attachments/assets/310a5c32-b3a8-4889-bca9-0364a6f1d1d7" />

Specifically, using the example `nginx.conf`, we have the following setup:

- Merged: `switch.cdn.fortheusers.org` (CDN for `magnezone.fortheusers.org`)
    - Primary: `switch2.cdn.fortheusers.org` (CDN for [switch-hbas-repo](https://github.com/fortheusers/switch-hbas-repo))
    - Secondary: `switch1.cdn.fortheusers.org` (CDN for `switchbru.com/appstore`)

The top-level `switch.cdn.fortheusers.org` domain is ultimately what is presented to/used by both the console and web HBAS clients.

For more info on that endpoint, see [hb-app.store/api-info](https://hb-app.store/api-info).

### License
MIT!
