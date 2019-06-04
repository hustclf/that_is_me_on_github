# that_is_me_on_github

that_is_me_on_github is a Python CLI application used for collect user's github contribution and generate markdown.

*The project is under actively development, not able to use. Welcome issue and pr to make it come true asap.

## Basic setup

Install the requirements:
```
$ pip install -r requirements.txt
```

Run the application:
```
$ python -m that_is_me_on_github generate --username hustclf --org_filter apache --repo_filter hustclf/RateLimiter,ing-bank/flink-deployer,edenhill/kafkacat
```


## Notice:
--auth_username and --auth_password are optional parameters. 
Without auth info, it is easily to reach the rate limit of github api, you can provide your account to avoid it.