from dataclasses import dataclass
from pathlib import Path
import time
import httpx


@dataclass
class Password:
    hashed: str
    plain: str
    cracked: bool = False
    cracked_at: float | None = None
    cracked_by: str | None = None

    def __str__(self):
        return f"Password(hashed={self.hashed}, plain={self.plain}, cracked={self.cracked}, cracked_at={self.cracked_at}, cracked_by={self.cracked_by})"

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return hash(self.hashed)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Password):
            return False
        return self.__hash__() == value.__hash__()

    def crack(self, cracked_by: str):
        self.cracked = True
        self.cracked_at = time.time()
        self.cracked_by = cracked_by

    def to_dict(self):
        return {
            "hashed": self.hashed,
            "plain": self.plain,
            "cracked": self.cracked,
            "cracked_at": self.cracked_at,
            "cracked_by": self.cracked_by,
        }

    @classmethod
    def from_string(cls, string):
        hashed, plain = string.split(":")
        return cls(hashed, plain)


@dataclass
class Potfile:
    potfile_path: Path
    last_modified: float | None = None
    last_read: float | None = None

    def __str__(self):
        return f"Potfile(potfile_path={self.potfile_path}, last_modified={self.last_modified}, last_read={self.last_read})"

    def __repr__(self):
        return str(self)

    def read(self):
        with self.potfile_path.open() as f:
            return f.read()

    def to_dict(self):
        return {
            "potfile_path": str(self.potfile_path),
            "last_modified": self.last_modified,
            "last_read": self.last_read,
        }


@dataclass
class Webhook:
    url: str
    username: str | None = None
    avatar_url: str | None = None

    def __str__(self):
        return f"Webhook(url={self.url}, username={self.username}, avatar_url={self.avatar_url})"

    def __repr__(self):
        return str(self)

    def send(self, content: dict):
        return httpx.post(self.url, json=content)

    def to_dict(self):
        return {
            "url": self.url,
            "username": self.username,
            "avatar_url": self.avatar_url,
        }
