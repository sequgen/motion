import pytest
import numpy
from motion.motion import motion_6d


def test_stationary():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 0])

    channels = motion_6d(t, x, y, z)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(-1, abs=1e-2), "did not expect acceleration other than g in z"


def test_freefall_from_stationary():

    # time
    t = numpy.asarray([0, 4.515])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([100, 0])

    channels = motion_6d(t, x, y, z)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(0, abs=1e-2), "expected zero g while freefalling"


def test_freefall_with_initial_velocity():

    # time
    t = numpy.asarray([0, 3.6095])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([100, 0])

    vz0 = -10.0

    channels = motion_6d(t, x, y, z, vz0=vz0)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(0, abs=1e-2), "expected zero g while freefalling"


def test_with_initial_upward_velocity_but_no_acceleration():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 10])

    channels = motion_6d(t, x, y, z, vz0=10.0)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(-1), "did not expect acceleration other than g in z"


def test_with_initial_downward_velocity_but_no_acceleration():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([10, 0])

    channels = motion_6d(t, x, y, z, vz0=-10.0)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(-1), "did not expect acceleration other than g in z"


def test_with_initial_downward_velocity_but_no_acceleration_more_steps():

    # time
    t = numpy.asarray([0, 1, 2])

    # position
    x = numpy.asarray([0, 0, 0])
    y = numpy.asarray([0, 0, 0])
    z = numpy.asarray([20, 10, 0])

    channels = motion_6d(t, x, y, z, vz0=-10.0)

    assert channels[0][1:] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1:] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1:] == pytest.approx(-1), "did not expect acceleration other than g in z"


def test_with_initial_downward_velocity_and_gravitational_acceleration_more_steps():

    # time
    t = numpy.asarray([0, 3.6095, 3.6095 + 1.8375])

    # position
    x = numpy.asarray([0, 0, 0])
    y = numpy.asarray([0, 0, 0])
    z = numpy.asarray([200, 100, 0])

    channels = motion_6d(t, x, y, z, vz0=-10.0)

    assert channels[0][1:] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1:] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1:] == pytest.approx(0, abs=1e-3), "expected zero g in z while freefalling"


def test_accelerate_decelerate():

    # time
    t = numpy.asarray([0, 2, 4])

    # position
    x = numpy.asarray([0, 0, 0])
    y = numpy.asarray([0, 0, 0])
    z = numpy.asarray([0, 9.81, 9.81])

    channels = motion_6d(t, x, y, z)

    assert channels[0][1:] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1:] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(-1.5), "expected half an extra g in z while accelerating"
    assert channels[2][2] == pytest.approx(0), "expected zero g in z"


def test_stationary_rotate_by_one_pi_around_x():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 0])

    rx = numpy.asarray([0, 1]) * numpy.pi

    channels = motion_6d(t, x, y, z, rx=rx)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(1), "did not expect acceleration other than upside-down g in z"


def test_stationary_rotate_by_one_pi_around_y():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 0])

    ry = numpy.asarray([0, 1]) * numpy.pi

    channels = motion_6d(t, x, y, z, ry=ry)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(1), "did not expect acceleration other than upside-down g in z"


def test_stationary_rotate_by_one_pi_around_z():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 0])

    rz = numpy.asarray([0, 1]) * numpy.pi

    channels = motion_6d(t, x, y, z, rz=rz)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(-1), "did not expect acceleration other than g in z"


def test_stationary_rotate_by_half_pi_around_x():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 0])

    rx = numpy.asarray([0, 0.50]) * numpy.pi

    channels = motion_6d(t, x, y, z, rx=rx)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(-1), "expected g to show up in y"
    assert channels[2][1] == pytest.approx(0), "did not expect g in z"


def test_stationary_rotate_by_half_pi_around_y():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 0])

    ry = numpy.asarray([0, 0.5]) * numpy.pi

    channels = motion_6d(t, x, y, z, ry=ry)

    assert channels[0][1] == pytest.approx(1), "expected g to show up in x, but with opposite sign"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(0), "did not expect g in z"


def test_stationary_rotate_by_half_pi_around_z():

    # time
    t = numpy.asarray([0, 1])

    # position
    x = numpy.asarray([0, 0])
    y = numpy.asarray([0, 0])
    z = numpy.asarray([0, 0])

    rz = numpy.asarray([0, 0.5]) * numpy.pi

    channels = motion_6d(t, x, y, z, rz=rz)

    assert channels[0][1] == pytest.approx(0), "did not expect g in x"
    assert channels[1][1] == pytest.approx(0), "did not expect g in y"
    assert channels[2][1] == pytest.approx(-1), "did not expect acceleration other than g in z"
