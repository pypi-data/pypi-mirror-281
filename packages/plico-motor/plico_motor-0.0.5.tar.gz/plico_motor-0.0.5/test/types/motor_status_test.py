import unittest
from plico_motor.types.motor_status import MotorStatus
from plico_motor.client.snapshot_entry import SnapshotEntry


class Test(unittest.TestCase):

    def setUp(self):
        self.ms = MotorStatus(
            'pippo',
            123,
            42.0,
            987654,
            False,
            MotorStatus.TYPE_ROTARY,
            True,
            333,
            1)

    def test_as_dict(self):
        wanted_keys = (
            SnapshotEntry.MOTOR_NAME,
            SnapshotEntry.POSITION,
            SnapshotEntry.VELOCITY,
            SnapshotEntry.STEPS_PER_SI_UNITS,
            SnapshotEntry.WAS_HOMED,
            SnapshotEntry.MOTOR_TYPE,
            SnapshotEntry.IS_MOVING,
            SnapshotEntry.LAST_COMMANDED_POSITION,
            SnapshotEntry.AXIS_NO)
        got = self.ms.as_dict()
        self.assertCountEqual(got.keys(), wanted_keys)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
