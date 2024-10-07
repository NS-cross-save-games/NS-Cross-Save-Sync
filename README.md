# NS-Cross-Save-Sync (under development)

A tool to sync save files between Nintendo Switch and PC.

You can use [JKSV](https://github.com/J-D-K/JKSV) to export and upload zipped switch saves, then convert and sync PC saves with NS-Cross-Save-Sync. Or conversely, convert PC saves to zipped switch saves (*note that due to the current limitations of JKSV, only same-name overwriting is possible*).

A best practice is to mount webdav locally and use NS-Cross-Save-Sync for bidirectional save synchronization.

## run

```bash
git clone https://github.com/NS-cross-save-games/NS-Cross-Save-Sync.git
cd dist
./main.exe
```

Or

```bash
git clone https://github.com/NS-cross-save-games/NS-Cross-Save-Sync.git
pip install -r requirements.txt
python main.py
```

## Supported games list

- [x] Disco Elysium
- [x] The Witcher 3
- [x] Balatro
