# TL;DR

A "slim" build of jupyter `scipy-notebook`.  Basically the same as `../jupyter/`, but without all the `Rlang` packages that make that image such a monster to build.

## Run locally

```
docker-compose -f ./jupyterslim.yaml up
```

Then connect to http://localhost:9880/lw-workspace/proxy/

## Deploy to hatchery

```
manifestFolder="$whatever/cdis-manifest/your.commons/manifests/hatchery"
cp jupyterslim.yaml "$manifestFolder/"
appdata="$(
  cat - <<EOM
    {
      "type": "dockstore-compose:1.0.0",
      "path": "/hatchery-more-configs/jupyterslim.yaml",
      "name": "Gen3_Slim_Jupyter_Notebook"
    }
EOM
)"
if jq --argjson appdata "$appdata" '.["more-configs"] |= . + [$appdata]' < "$manifestFolder/hatchery.json" > "$manifestFolder/hatcheryNew.json"; then
  mv "$manifestFolder/hatcheryNew.json" "$manifestFolder/hatchery.json"
fi

```

## Version

Run `jupyter --version` in a terminal to get version information:

```
$ jupyter --version
jupyter core     : 4.6.3
jupyter-notebook : 6.0.3
qtconsole        : not installed
ipython          : 7.15.0
ipykernel        : 5.3.0
jupyter client   : 6.1.3
jupyter lab      : 2.1.3
nbconvert        : 5.6.1
ipywidgets       : 7.5.1
nbformat         : 5.0.6
traitlets        : 4.3.3
```

Note: the versions shown above may not apply to current image versions.
