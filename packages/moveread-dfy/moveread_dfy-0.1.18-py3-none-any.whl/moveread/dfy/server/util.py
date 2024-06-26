from time import time
from fastapi import Request

def from_lichess(req: Request):
  return 'lichess' in req.headers.get('User-Agent', '')

def clientId(req: Request) -> str | None:
  """Client's Host, fallbacked to User-Agent"""
  return req.client.host if req.client else req.headers.get('User-Agent')

class Throttler:
  def __init__(self, max_entries: int, ttl_secs: float):
    self.last_accesses: dict[str, float] = {}
    self.max_entries = max_entries
    self.ttl_secs = ttl_secs

  def insert(self, client: str, access_time: float):
    if len(self.last_accesses) >= self.max_entries:
      older_client = min(self.last_accesses.keys(), key=self.last_accesses.__getitem__)
      del self.last_accesses[older_client]
    self.last_accesses[client] = access_time

  def throttle(self, client: str) -> bool:
    now = time()
    if not client in self.last_accesses:
      self.insert(client, now)
      return False
    elif now - self.last_accesses[client] > self.ttl_secs:
      self.insert(client, now)
      return False
    else:
      delta = now - self.last_accesses[client]
      print(f'Last accessed {delta:.2f} secs ago by {client}')
      return True