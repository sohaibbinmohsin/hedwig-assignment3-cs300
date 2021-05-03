import unittest
from hedwig import Hedwig
from hedwigmsg import Hedwigmsg
from delivery import MsgCreation, Send
from hashutils import encoded_hash_object

class HedwigTest(unittest.TestCase):
    def test_genesis_is_included(self):
        hedwig = Hedwig()
        self.assertEqual(len(hedwig.blockchain.blocks), 1)

    def test_msg_creation(self):
        hedwig = Hedwig()
        msgs = [
            Hedwigmsg(value=2, inbox_id=hedwig.inbox.id),
            Hedwigmsg(value=5, inbox_id=hedwig.inbox.id)
        ]
        hedwig.create_msgs(msgs)
        self.assertTrue(isinstance(hedwig.blockchain.blocks[1].delivery,
            MsgCreation))

    def test_process_send_without_signature(self):
        """ Put msgs in Hedwig's inbox, and transfer them
            to the same inbox without signing
        """
        hedwig = Hedwig()
        msg = Hedwigmsg(value=2, inbox_id=hedwig.inbox.id)
        created_msgs = hedwig.create_msgs([msg]).delivery.created_msgs
        send = Send(created_msgs=[msg], deleted_msgs=created_msgs)
        send_result = hedwig.process_send(send, [])
        self.assertEqual(send_result, None)

    def test_process_send_with_signature(self):
        """ Put msgs in Hedwig's inbox, and transfer them
            to the same inbox
        """
        hedwig = Hedwig()
        msg = Hedwigmsg(value=2, inbox_id=hedwig.inbox.id)
        created_msgs = hedwig.create_msgs([msg]).delivery.created_msgs
        send = Send(created_msgs=[msg], deleted_msgs=created_msgs)
        signature = hedwig.inbox.sign(encoded_hash_object(send))
        send_result = hedwig.process_send(
            send, [(hedwig.inbox.verifying_key, signature)]
        )
        self.assertFalse(send_result == None)

if __name__ == '__main__':
    unittest.main()
