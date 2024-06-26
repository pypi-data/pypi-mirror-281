# Nautobot UUID Lookup Plugin

Simple plugin to redirect existing UUIDs to the according object pages. Queries all nautobot `BaseModels`s. Fails if the models have no `get_absolute_url` method.

## Website
Usage: `https://your-nautobot-instance.com/plugins/uuid/YOUR-UUID-HERE`

## API
Usage: `https://your-nautobot-instance.com/api/plugins/uuid/YOUR-UUID-HERE`
