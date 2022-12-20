# JCOIN Browser App

The raw data used by this app should not be accessible to users. Users should only be able to see the aggregated data displayed by the app.

The raw data file has been encrypted with a secret passphrase before being indexed in Gen3. Users may be able to download it, but not to decode it. Only the app has the secret passphrase necessary to decode it.

The secret passphrase is configured as a GitHub secret and injected in a `secrets.toml` file before the app image is built.

To configure this app as a Gen3 workspace:
```
> hatchery.json
{
    ...
    "containers": [
        {
            "name": "Browser App",
            "image": "quay.io/cdis/jcoin-browser-app:master",
            "target-port": 8888,
            "cpu-limit": "0.50",
            "memory-limit": "256Mi",
            "env": {
                "DISABLE_AUTH": "true",
                "NAMESPACE": "<namespace>"
            },
            "path-rewrite": "/",
            "ready-probe": "/",
            "use-tls": "false"
        },
        ...
    ]
}
```
