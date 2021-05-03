from delivery import Delivery, MsgCreation, Send
from hashutils import hash_sha256
from base64 import b64encode
from hedwigmsg import MsgId

class Blockchain():
    """ Blockchain is composed by the blockchain itself
        (represented as an array of blocks), and a series
        of functions to manage it.
    """
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        """ Add a block to the blockchain.
            HINTS: 
            - A block will have multiple messages, each delivery will have its own id and each message will have its own id
            - ids can be any unique arbitrary number (like the count)
            - A block in the blockchain includes the hash of the previous block
            - Sending a message (delivery) is like a transaction
            - Check Block class for further info
            - You can use the hashfunction implemnted in hashutils
            Return the hash of the block.
        """
        """""""""""""""""""""
        YOUR CODE STARTS HERE
        """""""""""""""""""""
        

        """""""""""""""""""""
        YOUR CODE ENDS HERE
        """""""""""""""""""""
        self.blocks.append(block)
        return block

    def check_blockchain(self):
        """ Check the blockchain to find inconsistencies 
            HINTS:
            - A consistent BC will have atleast one block
            - Return true if all the blocks are valid 
            - Return false otherwise

        """

        """""""""""""""""""""
        YOUR CODE STARTS HERE
        """""""""""""""""""""
       
        """""""""""""""""""""
        YOUR CODE ENDS HERE
        """""""""""""""""""""

        return True

    def check_msg(self, msg):
        """ Check if the msg was created and was not deleted """
        creation_id = msg.id.delivery_id

        # Check created
        if msg not in self.blocks[creation_id].delivery.created_msgs:
            print('WARNING: Msg creation not found')
            return False

        # Check no duplicate
        for ind in range(creation_id + 1, len(self.blocks)):
            delivery = self.blocks[ind].delivery
            if isinstance(delivery, Send) and msg in delivery.deleted_msgs:
                print('WARNING: Duplicate detected')
                return False

        return True

    def check_msgs(self, msgs):
        """ Check a group of msgs. If the check_msg function
            returns false for any of the msgs then the result is
            false, otherwise the result is true.
        """
        for msg in msgs:
            if not self.check_msg(msg):
                return False
        return True

    def get_hash_last_block(self):
        """ Return the hash of the last block of the
            blockchain. If there are not blocks, return
            None.
        """
        blocks = self.blocks
        if len(blocks) > 0:
            return hash_sha256(blocks[-1])
        else:
            return None

    def __str__(self):
        separator = '-' * 30 + '\n'
        concat = 'Blockchain \n' + separator
        for block in self.blocks:
            concat += str(block) + separator
        return concat

class Block():
    """ Node of the blockchain """
    def __init__(self, delivery, hash_previous_block=None):
        self.delivery = delivery
        self.hash_previous_block = hash_previous_block

    def __str__(self):
        return 'Block: ' + str(self.delivery.id) + \
            '\tHash previous block: ' + str(self.hash_previous_block) + '\n' + \
            str(self.delivery)
