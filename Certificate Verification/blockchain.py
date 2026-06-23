import hashlib
import datetime


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block("Genesis Block")

    def create_block(self, data):

        previous_hash = self.chain[-1]["hash"] if self.chain else "0"

        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "data": data,
            "previous_hash": previous_hash
        }

        block["hash"] = hashlib.sha256(str(block).encode()).hexdigest()

        self.chain.append(block)

        return block