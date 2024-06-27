from sqlite3 import connect
from base64 import b64decode
from pathlib import Path
from json import load
from Crypto.Cipher import AES
from sqlime3.shell import Lime
from win32crypt import CryptUnprotectData


def decrypt_value(key, encrypted_value):
    iv = encrypted_value[3:15]
    encrypted_value = encrypted_value[15:]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    return cipher.decrypt(encrypted_value)[:-16].decode()


class Biscuit:
    def __init__(self, user_data_dir, profile='Default'):
        self._user_data_dir = Path(user_data_dir)

        local_state = self._user_data_dir / 'Local State'
        with open(local_state, "r", encoding='latin-1') as file:
            local_state = load(file)
        key = b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        self._key = CryptUnprotectData(key, None, None, None, 0)[1]

        cookies_path = self._user_data_dir / profile / 'Network' / 'Cookies'
        if not cookies_path.exists():
            raise FileNotFoundError(cookies_path)
        self._conn = connect(cookies_path)
        self._lime = Lime(self._conn)

    def columns(self):
        return self._lime['cookies'].columns.names

    def rows(self, item=None):
        table = self._lime['cookies']
        rows = table.rows[item] if item else table.rows
        cookies = [list(row) for row in rows]
        for cookie in cookies:
            if not (cookie[5] or isinstance(cookie[5], bytes)):
                continue
            if not cookie[5].startswith(b'v10'):
                cookies.remove(cookie)
                continue
            cookie[4] = decrypt_value(self._key, cookie[5])
            cookie[5] = ''
        return [dict(zip(self.columns(), cookie)) for cookie in cookies]

    def insert(self, *args, **kwargs):
        return self._lime['cookies'].rows.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._lime['cookies'].rows.delete(*args, **kwargs)
