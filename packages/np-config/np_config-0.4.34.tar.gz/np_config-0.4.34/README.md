# np_config


### *For use on internal Allen Institute network*

## Usage

Fetch configs from ZooKeeper nodes or .yaml/.json files:

```python
import np_config

zk_config: dict[str, str | int] = np_config.from_zk('/rigs/NP.1')

file_config: dict[str, Any] = np_config.from_file('local_config.yaml')

```


If running on a machine attached to a Mindscope Neuropixels rig (`NP.0`, ..., `NP.3`), get rig-specific config info with:

```python
rig = np_config.Rig()

name: str = rig.id                            # "NP.1"
index: int = rig.idx                          # 1

acquisition_pc_hostname: str = rig.acq        # "W10DT713843"
config: dict[str, str | int] = rig.config     # specific to NP.1
paths: dict[str, pathlib.Path] = rig.paths    # using values from rig.config
```



If not running on a rig-attached machine, get the config for a particular rig by supplying rig-index as an `int` to `Rig`:

```python
np1 = np_config.Rig(1)

np1_mvr_data_root: pathlib.Path = np.paths['MVR']
```


***


- the Mindscope ZooKeeper server is at `eng-mindscope:2181`
- configs can be added via ZooNavigator webview:
  [http://eng-mindscope:8081](http://eng-mindscope:8081)
- or more conveniently, via an extension for VSCode such as [gaoliang.visual-zookeeper](https://marketplace.visualstudio.com/items?itemName=gaoliang.visual-zookeeper)

## Development
Initialize for local development

```bash
poetry install --with dev
```

Run the tests

```bash
poetry run pytest
```
