from blockchain import Blockchain, Block
from ecdsa import SigningKey
from delivery import MsgCreation
from hashutils import hash_sha256, hash_object, encoded_hash_object
from hedwigmsg import Hedwigmsg, MsgId
from inbox import Inbox

class Hedwig():
    """ Trusted entity that creates and manages the blockchain """
    def __init__(self):
        self.inbox = Inbox()
        self.blockchain = Blockchain()
        self.genesis_block_hash = hash_object(self.add_genesis_block())
        self.last_block_signature = self.inbox.sign(
            self.genesis_block_hash.encode('utf-8')
        )

    def add_genesis_block(self):
        """ Add the genesis block to the blockchain and return
            the hash of the genesis block
        """
        msg = Hedwigmsg(1, self.inbox.id, MsgId(0,0))
        return self.create_msgs([msg])

    def create_msgs(self, msgs):
        """ Add a MsgCreation delivery to the blockchain
            that creates the msgs passed as parameters.
            Return the hash of the added block.
        """
        delivery = MsgCreation(created_msgs=msgs)
        block = Block(delivery)
        return self.blockchain.add_block(block)

    def process_send(self, send, signatures):
        """ Process a send sent by a user.
            The paramenter signatures is a list of duples with
            the users' validation keys as the first component
            and the send signatures as the second component.
        """
        # Verify users' signatures
        if (not self.verify_signatures(send, signatures) or
                not send.verify_balance()):
            return None

        # Check if all the msgs that are being transferred
        # exist and were not deleted previously
        if (not self.blockchain.check_msgs(send.deleted_msgs)):
            return None

        block = Block(send)
        return self.blockchain.add_block(block)

    def verify_signatures(self, delivery, signatures):
        """ Verify a list of delivery signatures """
        
        for verifying_key, signature in signatures:
            if not self.inbox.verify_signature(
                    verifying_key, signature, encoded_hash_object(delivery)):
                return False

    
        users = []
        for verifying_key, signature  in signatures:
            inbox_id = self.inbox.get_inbox_id_from_verifying_key(verifying_key)
            users.append(inbox_id)
        for msg in delivery.deleted_msgs:
            if msg.inbox_id not in users:
                return False

        return True
