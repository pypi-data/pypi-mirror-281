from typing import List

from pydantic import BaseModel, Field

class ChunkJoiner(BaseModel):
    chunks: List[str] = Field(default_factory=list,
                              min_items=1)

    def join_chunks(self) -> str:
        if not self.chunks:
            return ""

        # pylint: disable=E1136
        parts = [self.chunks[0]]
        for i in range(1, len(self.chunks)):
            prev_chunk = self.chunks[i-1]
            curr_chunk = self.chunks[i]
            # Determine maximum overlap using a dictionary to track prev_chunk suffixes
            overlap_length = 0
            prev_suffixes = {prev_chunk[-j:]: j for j in range(1, len(prev_chunk) + 1)}
            for j in range(1, len(curr_chunk) + 1):
                if curr_chunk[:j] in prev_suffixes:
                    overlap_length = prev_suffixes[curr_chunk[:j]]
            # Append non-overlapping part of the current chunk
            parts.append(curr_chunk[overlap_length:])

        # Join all parts at once for efficiency
        return ''.join(parts)
