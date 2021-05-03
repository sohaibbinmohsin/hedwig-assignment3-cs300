class Hedwigmsg():
    """ Each msg has an id, a value that is how many hedwigmsgs
        it represents, and a inbox id that is its owner.

        The msg id is assigned by Hedwig when the delivery
        that creates the msg is included in the blockchain.
    """
    def __init__(self, value, inbox_id, msg_id=None):
        self.value = value
        self.inbox_id = inbox_id
        self.id = msg_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        if self.id != None:
            num = self.id.msg_num
        else:
            num = 'N/A'
        return 'Num: ' + str(num) + ', Value: ' + str(self.value) + \
            ', Inbox id: ' + self.inbox_id

class MsgId():
    """ The id of a msg. It has two properties:
        - delivery_id: the index of the block where the
            delivery is included.
        - msg_num: the index of the msg into the delivery.
    """
    def __init__(self, msg_num, delivery_id=None):
        self.msg_num = msg_num
        self.delivery_id = delivery_id
