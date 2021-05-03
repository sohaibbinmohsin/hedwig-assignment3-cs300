from hashutils import hash_sha256
from ecdsa import SigningKey

class Delivery():
    """ Generic msg delivery """
    pass

class Send(Delivery):
    """ Transfer msgs between inboxs """
    def __init__(self, created_msgs, deleted_msgs, delivery_id=-1):
        self.created_msgs = created_msgs
        self.deleted_msgs = deleted_msgs
        self.id = delivery_id

    def verify_balance(self):
        """ Verify that the total count of created msgs is
            equal to the total count of deleted msgs
        """
        total_created = 0
        total_deleted = 0

        for deleted_msg in self.deleted_msgs:
            total_deleted += deleted_msg.value
        for created_msg in self.created_msgs:
            total_created += created_msg.value
        return total_deleted == total_created

    def __str__(self):
        concat = 'TransID: ' + str(self.id) + '\t' + 'Type: Send\n' + \
            '\nDeleted msgs: \n'
        for msg in self.deleted_msgs:
            concat += str(msg) + '\n'
        concat += '\nCreated msgs: \n'
        for msg in self.created_msgs:
            concat += str(msg) + '\n'
        return concat

class MsgCreation(Delivery):
    """ Creation of msgs """
    def __init__(self, created_msgs, delivery_id=-1):
        self.created_msgs = created_msgs
        self.id = delivery_id

    def __str__(self):
        concat = 'TransID: ' + str(self.id) + '\t' + 'Type: Msg creation\n' + \
            '\nCreated msgs: \n'
        for msg in self.created_msgs:
            concat += str(msg) + '\n'
        return concat
