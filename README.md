# Web interface for PDF overlay

## How to start
This uses pdfrw, Flask and Python 3.6.

For pkgsrc users, please run as follows.

```
$ cd ~/pdf-overlay
$ git clone git@github.com:ryoon/pdf-overlay-web-ui.git app
$ cd pkgsrc/bootstrap
$ ./bootstrap --workdir /tmp/bs --unprivileged --prefix ~/pdf-overlay/pkg
$ echo PYTHON_VERSION_DEFAULT=36 >> ~/pdf-overlay/pkg/etc/mk.conf
$ cd pkgsrc/www/py-flask
$ ~/pdf-overlay/pkg/bin/bmake install
$ cd pkgsrc/textproc/py-pdfrw
$ ~/pdf-overlay/pkg/bin/bmake install
$ cd ~/pdf-overlay/app
$ LANG=ja_JP.UTF-8 ~/pdf-overlay/pkg/bin/python3.6 app.py
```

And open http://localhost:5000/ with your browser on localhost.

## Bugs
* Not secure for the internet use

## Plans
* Some improvements

## Contact
Ryo ONODERA <ryo@tetera.org>
