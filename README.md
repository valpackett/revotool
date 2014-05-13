# revotool [![](https://travis-ci.org/myfreeweb/revotool.png?branch=master)](https://travis-ci.org/myfreeweb/revotool) [![](https://pypip.in/d/revotool/badge.png)](https://pypi.python.org/pypi/revotool)

Revotool is a CLI tool for working with MODX Revolution™.
It allows you to use git to work on websites powered by this CMS.

## Features

- pulling elements
- pushing elements

### TODO

- rename support
- custom `/manager` directory support
- mock the http in tests

## Installation

```bash
$ [sudo] easy_install pip # if you don't have pip
$ [sudo] pip install revotool
```

## Usage

Starting:

```bash
$ revotool remote add production https://example.com adminUsername
$ revotool pull production
$ git init
$ git add -A
$ git commit
```

Pushing:

```bash
$ revotool push production
```
