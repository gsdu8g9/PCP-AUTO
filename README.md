# PCP-AUTO  beta.
Automatically group editor for social network OK.RU

> cron_file.py - entry point

----
- **OK.RU** api wrapper

	    from modules.ok_api import api_request
		api_request(method, params={})

- structure of **./access_config.py**

		APP_ID = ''
		PUBLIC_KEY = ''
		SECRET_KEY = ''
		ACCESS_TOKEN = ''
		SECRET_SESSION_KEY = ''