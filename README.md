# BackupFtp

Create automatic ftp backup and upload to gitlab

- [x] Sync files and folders locally from remote ftp
- [x] Automatic commit
- [x] Upload changes to gitlab, github
- [x] Generate error log file

# Usage

```bash
git clone https://github.com/juliandavidmr/BackupFtp.git
cd BackupFtp
python main.py
```

> Configure the FTP credentials in the [conf](conf.py) file

_Successfully tested with python v2.7.13_