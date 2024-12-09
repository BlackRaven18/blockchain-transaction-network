from clients.logger import log, MessageType

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
class ErrorFlags(metaclass=SingletonMeta):
    def __init__(self):
        self._node_damage_error = False
        self._transaction_vote_error = False
        self._block_mining_error = False

    async def set_node_damage_error(self) -> str:
        self._node_damage_error = True
        await log(MessageType.NODE_DAMAGE_ERROR)

        return "Node damage error set"

    async def reset_node_damage_error(self) -> str:
        self._node_damage_error = False
        await log(MessageType.IDLE)

        return "Node damage error reset"
    
    def set_transaction_vote_error(self) -> str:
        self._transaction_vote_error = True

        return "Transaction vote error set"

    def reset_transaction_vote_error(self) -> str:
        self._transaction_vote_error = False

    def set_block_mining_error(self) -> str:
        self._block_mining_error = True

        return "Block mining error set"
    
    def reset_block_mining_error(self) -> str:
        self._block_mining_error = False

    @property
    def node_damage_error(self):
        return self._node_damage_error
    
    @property
    def transaction_vote_error(self):
        return self._transaction_vote_error
    
    @property
    def block_mining_error(self):
        return self._block_mining_error
    
    def serialize(self):
        return self.__dict__
