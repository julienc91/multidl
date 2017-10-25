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

Description
-----------

With `multidl`, download multiple files in parallel from a single command line.
`multidl` currently supports the following protocols:

* local files
* ftp
* http
* https

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

    multidl -c urls.txt -o /tmp -n 3
    
You can also give the targeted urls to `multidl` via `stdin` like so:

    cat urls.txt | multidl -o /tmp -n 3
