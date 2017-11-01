[![Build Status](https://travis-ci.org/julienc91/multidl.svg?branch=master)](https://travis-ci.org/julienc91/multidl)
[![codecov](https://codecov.io/gh/julienc91/multidl/branch/master/graph/badge.svg)](https://codecov.io/gh/julienc91/multidl)

multidl
=======

Download files from anywhere in parallel.

* Author: Julien CHAUMONT (https://julienc.io)
* Version: 0.1
* Date: 2017-10-15
* Licence: MIT
* Url: http://github.com/julienc91/multidl

Demo
----

![Demo](https://github.com/julienc91/multidl/blob/master/docs/demo.gif)

Description
-----------

With `multidl`, download multiple files in parallel from a single command line.
`multidl` currently supports the following protocols:

* local files
* ftp
* http
* https

There is also a special treatment for the following platforms:

* YouTube

Install
-------

One simple command line:

    python setup.py install

Usage
-----

Gather the urls of the targeted files in a single configuration file:

```
http://example.com/file1.txt
https://megamovies.org/bestmovieever.mkv
ftp://me:passw0rd@ftpserver.com/dir/file2.txt
```

Then launch `multidl`:

    multidl -c urls.txt -o downloads/
    
You can also give the targeted urls to `multidl` via `stdin` like so:

    cat urls.txt | multidl -o downloads/
