# statit_py
A package to access the [Statit](https://gostatit.com) API

## Installation

To install the current release:

```
$ pip install statit_py
```

## Quick usage

To use the Statit REST API methods, first authenthicate yourself with your username and API token (see [Signing-in](https://help.gostatit.com/excel/signin/#authentication)):

```py
import statit_py

statitAPI = statit_py.coreAPI('<username>', '<api_key>')
```

`GET`, `LIST` and `DELETE` actions for collections and series are available in reference-by-ID format:

```py
data = statitAPI.getSerie('<serie_id>')
```

Alongside with the remaining `PUT` and all their respective `batch`  actions, they are also available in standard JSON request format:

```py
statitAPI.putSerieJSON({
    'id': '<serie_id>',
    ...
})
```

For the full list of methods and their detailed arguments, see the [Python Documentation]().






