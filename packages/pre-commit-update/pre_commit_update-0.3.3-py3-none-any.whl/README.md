<div align="center"><h1>pre-commit-update</h1>

![PyPI - Version](https://img.shields.io/pypi/v/pre-commit-update)
![PePy - Downloads](https://pepy.tech/badge/pre-commit-update)
![Gitlab Pipeline Status](https://img.shields.io/gitlab/pipeline-status/vojko.pribudic.foss%2Fpre-commit-update?branch=main&label=pipeline)
![GitLab Issues](https://img.shields.io/gitlab/issues/open/vojko.pribudic.foss%2Fpre-commit-update)
![GitLab Last Commit](https://img.shields.io/gitlab/last-commit/vojko.pribudic.foss%2Fpre-commit-update)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/pre-commit-update)
![Python - Formatter](https://img.shields.io/badge/code%20style-black-black)
![PyPI - License](https://img.shields.io/pypi/l/pre-commit-update?color=%23333333)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pre-commit-update)
![Codacy grade](https://img.shields.io/codacy/grade/e727532ea95341b18ffd963e77605c2b?logo=codacy)
</div>
<div align="center">
<a href="https://ko-fi.com/H2H8WN45E" target="_blank"><img alt="kofi" src="https://i.imgur.com/wdSRlJB.png" width="141" height="36"></a>

<strong>pre-commit-update</strong> is a simple CLI tool to check and update pre-commit hooks.
</div>

## Table of contents

1. [ Reasoning ](#1-reasoning)
2. [ Features ](#2-features)
3. [ Installation ](#3-installation)
4. [ Usage ](#4-usage)
    1. [ Pipeline usage example ](#1-pipeline-usage-example)
       1. [ GitLab job ](#a-gitlab-job)
    2. [ pre-commit hook usage example ](#2-pre-commit-hook-usage-example)
5. [ Configuration ](#5-configuration)

## 1. Reasoning

`pre-commit` is a nice little tool that helps you polish your code before releasing it into the wild.
It is fairly easy to use. A single `pre-commit-config.yaml` file can hold multiple hooks (checks) that will go through
your code or repository and do certain checks. The problem is that the file is static and once you pin your hook versions
after a while they get outdated.

`pre-commit-update` was created because there is no easy way to update your hooks by using
`pre-commit autoupdate` as it is not versatile enough.


## 2. Features

|                      Feature                       | pre-commit-update |            pre-commit autoupdate            |
|:--------------------------------------------------:|:-----------------:|:-------------------------------------------:|
|   Dry run (checks for updates, does not update)    |        Yes        |                     No                      |
|                Stable versions only                |        Yes        |                     No                      |
|         Exclude repo(s) from update check          |        Yes        | Workaround (updates only specified repo(s)) |
| Keep repo(s) (checks for updates, does not update) |        Yes        |                     No                      |
|           Update by hash instead of tag            |        Yes        |                     Yes                     |
|          Can be used as a pre-commit hook          |        Yes        |                     No                      |
|       Can be configured in `pyproject.toml`        |        Yes        |                     No                      |


## 3. Installation

`pre-commit-update` is available on PyPI:
```console 
$ python -m pip install pre-commit-update
```

**NOTE:** Please make sure that `git` is installed.


## 4. Usage

`pre-commit-update` CLI can be used as below:

```console
Usage: pre-commit-update [OPTIONS]

Options:
  -d, --dry-run / -nd, --no-dry-run             Dry run only checks for the new versions without updating  [default: nd]
  -a, --all-versions / -na, --no-all-versions   Include the alpha/beta versions when updating  [default: na]
  -v, --verbose / -nv, --no-verbose             Display the complete output  [default: nv]
  -p, --preview / -np, --no-preview             Previews the cli configuration values by overwriting order (disables the actual cli work if enabled!)  [default: np]
  -e, --exclude REPO_URL_TRIM                   Exclude specific repo(s) by the `repo` url trim
  -k, --keep REPO_URL_TRIM                      Keep the version of specific repo(s) by the `repo` url trim (still checks for the new versions)
  -h, --help                                    Show this message and exit.
```

If you want to just check for updates (without updating `pre-commit-config.yaml`), for example, you would use:
```console
$ pre-commit-update -d
```
or
```console
$ pre-commit-update --dry-run
```

**NOTE:** If you are to use the `exclude` or `keep` options, please pass the repo url trim as a parameter.
Keep in mind that if you have multiple hooks (id's) configured for a single repo and you `exclude` that repo,
**NONE** of the hooks will be updated, whole repo will be excluded.

Example of repo url trim: https://github.com/ambv/black -> `black` (you will only pass `black` as a parameter to
`exclude` or `keep`)

### 1) Pipeline usage example
#### a) GitLab job:

```yaml
pre-commit-hooks-update:
  stage: update
  script:
    # install git if not present in the image
    - pip install pre-commit-update
    - pre-commit-update --dry-run
  except:
    - main
  when: manual
  allow_failure: true
```

**NOTE:** This is just an example, feel free to do your own configuration

### 2) pre-commit hook usage example

You can also use `pre-commit-update` as a hook in your `pre-commit` hooks:

```yaml
- repo: https://gitlab.com/vojko.pribudic.foss/pre-commit-update
  rev: v0.3.2  # Insert the latest tag here
  hooks:
    - id: pre-commit-update
      args: [--dry-run, --exclude, black, --keep, isort]
```

## 5. Configuration

You can configure `pre-commit-update` in your `pyproject.toml` as below (feel free to do your own configuration):

```toml
[tool.pre-commit-update]
dry_run = true
all_versions = false
verbose = true
preview = false
exclude = ["isort"]
keep = ["black"]
```

**NOTE:** If some of the options are missing (for example `exclude` option), `pre-commit-update`
will use default value for that option (default for `exclude` option would be an empty list).

***IMPORTANT*** If you invoke `pre-commit-update` with any arguments (e.g. `pre-commit-update -d`),
`pyproject.toml` configuration will be **overridden**. This means that all the arguments passed while
calling `pre-commit-update` will have priority over the configuration defined inside `pyproject.toml`.
If you want to override boolean flags, you can do so by passing the negative flag value.
For example, given the configuration above, to override `verbose` flag from `pyproject.toml`, you
would invoke `pre-commit-update` with either `--no-verbose` or `-nv`.

You can always check the configuration overrides (priorities) by running `pre-commit-update -p` / `pre-commit-update --preview`
