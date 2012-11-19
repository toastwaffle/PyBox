=====
PyBox
=====

An open-source, self hosted alternative to Dropbox

Watches for file system changes, uploads files to Amazon S3.
Requires a server to support syncing between multiple devices,
but can be used standalone as a backup solution. PyBox stores
each file separately and uncompressed, and history can be
customised (Keep all copies, keep last N copies, keep copies up
to N minutes/hours/days/months/years, keep N per minute/M per hour
etc.)

------------
Dependencies
------------

* watchdog
* boto
* path.py
* SQLAlchemy