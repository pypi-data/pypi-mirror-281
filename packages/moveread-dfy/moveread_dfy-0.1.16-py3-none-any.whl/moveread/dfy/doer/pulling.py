from typing import NamedTuple, Sequence
import asyncio
from sqlmodel import Session, select
from haskellian import either as E
from kv.api import KV

from moveread.dfy.types import Game, Pairing, SheetModel
from moveread.pipelines.dfy import Input

def pairing_display(pairing: Pairing):
  pair = pairing.root
  if pair.tag == 'unpaired':
    return 'Unpaired!?'
  
  s = f'{pair.white} - {pair.black}'
  if pair.result is not None:
    s += f' {pair.result}'
  return s


def title(pairing: Pairing, tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId} {group}/{round}/{board} {pairing_display(pairing)}'

class NewInput(NamedTuple):
  input: Input
  """Pipeline input"""
  urls: Sequence[str]
  """Blob URLs to be copied"""

def new_input(game: Game, *, model: str):
  gid = game.gameId()
  urls = [img.url for img in game.imgs]
  endpoint = f'/v1/models/{gid["tournId"]}-{gid["group"]}:predict'
  task = Input(gameId=gid, model=model, imgs=urls, title=title(game.pairing, **gid), serving_endpoint=endpoint)
  return NewInput(input=task, urls=urls)


def sheet_model(session: Session, tournId: str) -> str | None:
  stmt = select(SheetModel).where(SheetModel.tournId == tournId)
  obj = session.exec(stmt).first()
  return obj and obj.model


async def copy_images(
  urls: Sequence[str], *,
  online_images: KV[bytes], pipeline_images: KV[bytes]
):
  tasks = [online_images.copy(url, pipeline_images, url).run() for url in urls]
  results = await asyncio.gather(*tasks)
  return E.sequence(results)
