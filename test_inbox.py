import unittest
from inbox import Inbox
from hedwigmsg import Hedwigmsg
from hedwig import Hedwig
from delivery import MsgCreation
from hashutils import hash_object, encoded_hash_object

class TestInbox(unittest.TestCase):
    def test_devide_msg_in_two_msgs(self):
        """ Check that the msg division is done correctly """
        hedwig = Hedwig()
        inbox = Inbox()
        msg = Hedwigmsg(value=20, inbox_id=inbox.id)
        created_block = hedwig.create_msgs([msg])
        created_msgs = created_block.delivery.created_msgs
        new_msgs = inbox.devide_msg(
            msg=created_msgs[0], value=15, hedwig=hedwig
        )
        self.assertTrue(len(new_msgs) == 2)
        self.assertTrue(
            new_msgs[0].inbox_id == inbox.id and
            new_msgs[1].inbox_id == inbox.id
        )
        self.assertEqual(new_msgs[0].value + new_msgs[1].value, 20)

    def test_index_msg_with_value(self):
        inbox = Inbox()
        msgs = [
            Hedwigmsg(value=1, inbox_id=inbox.id),
            Hedwigmsg(value=2, inbox_id=inbox.id)]
        self.assertTrue(inbox.index_msg_value(msgs, 2) == 1)

    def test_get_msgs(self):
        hedwig = Hedwig()
        inbox1 = Inbox()
        inbox2 = Inbox()
        msgs = [
            Hedwigmsg(value=20, inbox_id=inbox1.id),
            Hedwigmsg(value=100, inbox_id=inbox2.id),
            Hedwigmsg(value=30, inbox_id=inbox1.id),

        ]
        hedwig.create_msgs(msgs)
        inbox_msgs = inbox1.get_msgs(hedwig.blockchain)
        self.assertEqual(len(inbox_msgs), 2)
        self.assertEqual(inbox_msgs[0].value + inbox_msgs[1].value, 50)

    def test_sign_and_verify(self):
        """ Sign a delivery and verify the signature """
        inbox = Inbox()
        msgs = [Hedwigmsg(value=2, inbox_id=inbox.id)]
        delivery = MsgCreation(created_msgs=msgs)
        encoded_hash = encoded_hash_object(delivery)
        self.assertTrue(
            inbox.verify_signature(
                inbox.verifying_key,
                inbox.sign(encoded_hash),
                encoded_hash
            )
        )

if __name__ == '__main__':
    unittest.main()
