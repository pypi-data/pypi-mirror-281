from typing import Mapping, Literal
from pydantic import BaseModel

class File(BaseModel):
  file: str
  compression: Literal['zstd'] | None = None
  num_lines: int | None = None

Meta = Mapping[str, File]

class MetaJson(BaseModel):
  lines_dataset: Meta