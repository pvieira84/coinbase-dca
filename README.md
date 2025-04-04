# Coinbase-DCA

[![Docker Hub package][dockerhub-badge]][dockerhub-link]

[dockerhub-badge]: https://img.shields.io/badge/images%20on-Docker%20Hub-blue.svg
[dockerhub-link]: https://hub.docker.com/repository/docker/pvieira84/coinbase-dca "Docker Hub Image"

Automate your DCA strategy by placing limit orders on Coinbase Advanced Trader for just below/above the spot price for your buys/sells.

## Setup

### Coinbase
Generate an API key (https://www.coinbase.com/settings/api) and give it permission to trade and view

## Run in Docker

```docker run -e COINBASE_KEY_NAME=YOUR_COINBASE_KEY -e COINBASE_KEY_SECRET=YOUR_COINBASE_TOKEN pvieira84/coinbase-dca```

### More Options
| Envs |Description  |
|--|--|
|**COINBASE_HOST**  | (optional) Coinbase API Host |
|**COINBASE_KEY_NAME**  | Your Coinbase API Key Name |
|**COINBASE_KEY_SECRET**  | Your Coinbase Private Key |
|**TRADING_PAIR**  | (optional) The trading pair to use for DCA |
|**ORDER_SIZE**  | (optional) The amount for DCA |
|**CRON_EXPRESSION**  | (optional) To run on a [Cron Schedule](https://crontab.guru/) |

## Contributing

* Feel free to submit any issue or PR's you think necessary
* If you like the work and want to buy me a coffee you are more than welcome :)

<a href="https://buymeacoffee.com/pvieira84" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
