# WARNING

You are reading the README and viewing the code for **v2**.

This code is incomplete and should not be used in production!

## Top.py

![issues: unresolved](https://img.shields.io/github/issues/dragdev-studios/top.py?style=for-the-badge)
![pull requests: unresolved](https://img.shields.io/github/issues-pr/dragdev-studios/top.py?style=for-the-badge)
![version: unresolved](https://img.shields.io/pypi/v/top.py?style=for-the-badge)
![supported python versions: unresolved](https://img.shields.io/pypi/pyversions/top.py?style=for-the-badge)
![downloads: unresolved](https://img.shields.io/pypi/dw/top.py?style=for-the-badge)
![code style: black](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge)
![discord.py version: 1.x, 2.0a](https://img.shields.io/badge/discord.py-1.x%20%7C%202.0a-blue?style=for-the-badge)

An alternative wrapper for the [top.gg API](//docs.top.gg)

_Please note, this is **not an official package from top.gg**. We are not
affiliated with top.gg in any way. If you want to install their official
package, please see [their repo](//github.com/top-gg/python-sdk)._

### Introduction

> Warning! top.py is not tested to be compatible with discord.py forks, or any other library than the official 
> discord.py library. If you encounter issues when using another library, please open an issue with as much detail
> and support will be added.

top.py is a python wrapper for the top.gg discord bot list API. top.py aims to
be object-oriented, whereas the official top.gg python SDK is more low-level raw
data.

#### Installation

You can install the latest stable release here:

```shell
pip install top.py
```

But, if you're reading this, you're most likely a developer - you should know
how to install packages by now.

#### Examples

You can see examples in the [examples.md](https://github.com/dragdev-studios/top.py/blob/master/examples.md) file.

#### Supported Features
<!-- Note to contributors: Use these emojis below 
<!-- ✅ ❌ -->

| Feature Name                        | Supported? |
| ----------------------------------- | ---------- |
| Automatic posting of server count   | ✅         |
| Searching/Bulk Querying Bots        | ✅         |
| Fetching a bot                      | ✅         |
| Fetching a user                     | ✅         |
| Fetching last 1000 upvotes          | ✅         |
| Fetching a bot's stats              | ✅         |
| Checking individual user vote       | ✅         |
| Manual posting server count         | ✅         |
| Models for all individual endpoints | ✅         |
| In-house ratelimiting               | ✅         |
| Vote Webhooks                       | ✅         |
| Making you a nice slice of toast    | ❌         |

**NOTE:** We do **NOT** currently provide official support for discord server
list. That's coming soon.

#### top.py features

* Object-Oriented (No-more shall you faff about with dictionaries)
* Sensible function names & arguments

### Useful links

[support](//discord.gg/YBNWw7nMGH) (or mention @eek#7574 in top.gg) |
[docs](//toppy.dragdev.xyz) | [PyPi](//pypi.org/project/top.py) |
[examples](/examples.md) | [\(META\) Code Of Conduct](/CODE_OF_CONDUCT.md) |
[\(META\) Contributing Guidelines](/CONTRIBUTING.md)

[Experiencing an issue?](/issues/new)
