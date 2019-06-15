# that_is_me_on_github
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![CircleCI](https://circleci.com/gh/hustclf/that_is_me_on_github.svg?style=svg)](https://circleci.com/gh/hustclf/that_is_me_on_github)
[![](https://images.microbadger.com/badges/image/hustclf/that_is_me_on_github.svg)](https://microbadger.com/images/hustclf/that_is_me_on_github "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/hustclf/that_is_me_on_github.svg)](https://microbadger.com/images/hustclf/that_is_me_on_github "Get your own version badge on microbadger.com")
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

that_is_me_on_github is a Python CLI application used for collect user's github contribution and generate markdown.

[demo](https://github.com/hustclf/that_is_me_on_github/blob/master/demo.md)

## Basic setup

Install the requirements:
```
$ pip install -r requirements.txt
```

Run the application:
```
$ python -m that_is_me_on_github generate --username hustclf --org_filter apache --repo_filter hustclf/RateLimiter,ing-bank/flink-deployer,edenhill/kafkacat
```
A markdown file named `that_is_me_on_github.md` will be generated under current folder.

## Docker Support
**Notice: docker will create a folder automatically when not exist. To aovid it, We should create an empty file manually.**

Run with docker
```
$ docker pull hustclf/that_is_me_on_github
$ touch ~/result.md
$ docker run -it --rm -v ~/result.md:/usr/src/that_is_me_on_github/that_is_me_on_github.mdhustclf/that_is_me_on_github generate --username hustclf --org_filter apache --repo_filter hustclf/RateLimiter,ing-bank/flink-deployer,edenhill/kafkacat > markdown.md
```

## Notice:
`--auth_username` and `--auth_password` are optional parameters. 
Without auth info, it is easily to reach the rate limit of github api, you can provide your account to avoid it.

For example:
```bash
$ python -m that_is_me_on_github generate --username hustclf --org_filter apache --repo_filter hustclf/RateLimiter,ing-bank/flink-deployer,edenhill/kafkacat \\ 
--do_auth True --auth_username <github_username> --auth_password <github password>
```
Replace <github_username> and <github_password> with your own.

## Development
that_is_me_on_github use pipenv for local development.

### 1. Install pipenv
```bash
$ pip install pipenv
```

### 2. Build a pipenv environment
```bash
$ cd path-to-the-project/
$ pipenv shell
```

### 3. Under development.
Pycharm is recommended ide.

### 4. Run tests.
```bash
$ pytest tests/
```
