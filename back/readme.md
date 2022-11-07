# Install cryptg python library

---
https://docs.telethon.dev/en/stable/basic/installation.html  
---
If cryptg is installed, the library will work a lot faster, since encryption and decryption will
be made in C instead of Python. If your code deals with a lot of updates or you are downloading/uploading
a lot of files, you will notice a considerable speed-up (from a hundred kilobytes per second to several
megabytes per second, if your connection allows it). If it’s not installed, pyaes will be used
(which is pure Python, so it’s much slower).
----
