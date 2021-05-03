from ecdsa import SigningKey
from hashutils import hash_sha256, hash_object, encoded_hash_object
from delivery import Send, MsgCreation
from hedwigmsg import Hedwigmsg
import pdb

class Inbox():
    """ A user of the hedwigmsg """
    def __init__(self, signing_key=None):
        if signing_key is None:
            self.signing_key = SigningKey.generate()
        else:
            self.signing_key = signing_key
        self.verifying_key = self.signing_key.get_verifying_key()
        self.id = self.get_inbox_id_from_verifying_key(
            self.verifying_key
        )

    def sign(self, message):
        """ Sign a message using the signing key """
        return self.signing_key.sign(message)

    def verify_signature(self, verifying_key, signature, message):
        """ Verify a signature of a message using the verifying key """
        return verifying_key.verify(signature, message)

    def get_inbox_id_from_verifying_key(self, verifying_key):
        """ Return the inbox key from the verifying key """
        return hash_object(verifying_key.to_string())

    def create_send(self, sends, blockchain, hedwig):
        """ Transfer msgs from this inbox to other(s).
            Parameters:
             - sends: List of duples (inbox id, count)
             - blockchain: The complete blockchain
             - hedwig: An interface to the Hedwig functions
        """
        deleted_msgs = []
        created_msgs = []
        my_msgs = self.get_msgs(blockchain)
        # TODO: Order msgs by their values

        for inbox_id, count in sends:
            my_msgs[:] = [
                msg for msg in my_msgs if msg not in deleted_msgs
            ]
            for msg in my_msgs:
                if msg.value <= count:
                    deleted_msgs.append(msg)
                    deleted_count = msg.value
                    count -= msg.value
                else:
                    new_msgs = self.devide_msg(msg, count, hedwig)
                    deleted_ind = self.index_msg_value(new_msgs, count)
                    deleted_msgs.append(new_msgs[deleted_ind])
                    deleted_count = count
                    my_msgs.append(new_msgs[deleted_ind + 1])
                    count = 0
                created_msgs.append(
                    Hedwigmsg(value=deleted_count, inbox_id=inbox_id)
                )
                if count == 0:
                    break
        return Send(created_msgs, deleted_msgs)

    def index_msg_value(self, msgs, value):
        """ Return the index of the first msg with the value
            passed as parameter
        """
        ind = 0
        while ind < len(msgs):
            if msgs[ind].value == value:
                return ind
            else:
                ind += 1
        return None

    def devide_msg(self, msg, value, hedwig):
        """ Devide a msg in two new msgs. The paramenter
            'value' is the value of one of the new msgs
            and the value of the other is the rest.
            The original msg is deleted and cannot be used
            again.
        """
        if value > msg.value:
            return
        created_msgs = []
        created_msgs.append(Hedwigmsg(value, self.id))
        created_msgs.append(Hedwigmsg(msg.value - value, self.id))
        send = Send(created_msgs=created_msgs, deleted_msgs=[msg])
        signature = self.sign(encoded_hash_object(send))
        new_block = hedwig.process_send(
            send, [(self.verifying_key, signature)]
        )
        return new_block.delivery.created_msgs

    def get_msgs(self, blockchain):
        """ Get all active msgs of the blockchain associated
            to this inbox
        """
        msgs = []
        for block in blockchain.blocks:
            tx = block.delivery
            for msg in tx.created_msgs:
                if msg.inbox_id == self.id:
                    msgs.append(msg)
            if isinstance(tx, MsgCreation):
                continue
            for msg in tx.deleted_msgs:
                if msg.inbox_id == self.id:
                    msgs.remove(msg)
        return msgs

    def __str__(self):
        """ String representations of the inbox """
        separator = '-' * 30 + '\n'
        concat = 'Inbox\n' + separator + \
            'Id: ' + self.id + '\n' + separator
        return concat
