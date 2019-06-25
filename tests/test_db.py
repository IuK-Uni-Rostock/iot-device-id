from lib.device_db import LocalDevice, DeviceType, DeviceTypeDB


def test_save_to_disk(tmp_path):
    DeviceTypeDB.db = None
    DeviceTypeDB.devices_location = tmp_path
    assert len(DeviceTypeDB.get_db().device_types) == 0
    dt = DeviceType("test_device")
    dt.add_characteristic("test", "R")
    DeviceTypeDB.get_db().add(dt)
    assert len(DeviceTypeDB.get_db().device_types) == 1
    DeviceTypeDB.db = None
    assert len(DeviceTypeDB.get_db().device_types) == 1
    print(DeviceTypeDB.get_db().device_types, dt, DeviceTypeDB.get_db().device_types.get(dt.uuid).characteristics)
    assert DeviceTypeDB.get_db().device_types.get(dt.uuid).characteristics == {("test", "R")}


def test_find_matching_device(tmp_path):
    DeviceTypeDB.devices_location = tmp_path
    DeviceTypeDB.db = None
    ld = LocalDevice("192.168.0.0")
    ld.add_characteristic("DNS", "('exmaple.com', 'A')")

    dt = DeviceType("test_device")
    dt.add_characteristic("DNS", "('exmaple.com', 'A')")

    dt_almost = DeviceType("not_the_right_device")
    dt_almost.add_characteristic("DNS", "('exmaple.com', 'A')")
    dt_almost.add_characteristic("XYZ", "('exmaple.com', 'A')")

    dt_bad = DeviceType("not_the_right_device")
    dt_bad.add_characteristic("ABC", "('asd.com', 'A')")

    DeviceTypeDB.get_db().add(dt)
    DeviceTypeDB.get_db().add(dt_bad)
    DeviceTypeDB.get_db().add(dt_almost)

    match = DeviceTypeDB.get_db().find_matching_device_type(ld)
    assert dt.characteristics == ld.characteristics
    assert match[1].name == dt.name
    assert match[0] == 1.0


def test_mkdir(tmp_path):
    DeviceTypeDB.devices_location = str(tmp_path) + "/devices"
    DeviceTypeDB.db = None
    dt = DeviceType("test_device")
    DeviceTypeDB.get_db().add(dt)


def test_str():
    str(DeviceType("test device"))


def test_fuzzy(tmp_path):
    DeviceTypeDB.devices_location = tmp_path
    DeviceTypeDB.db = None
    ld = LocalDevice("192.168.0.0")
    ld.add_characteristic("DNS", "('srv1.cloud.example.com', 'A')")
    ld.add_characteristic("MAC", "Example Inc.")

    dt_bad = DeviceType("test_device_bad")
    dt_bad.add_characteristic("DNS", "('iot.com', 'A')")
    dt_bad.add_characteristic("MAC", "Example Inc.")

    dt = DeviceType("test_device")
    dt.add_characteristic("DNS", "('srv2.cloud.example.com', 'A')")
    dt.add_characteristic("MAC", "Example Inc.")

    DeviceTypeDB.get_db().add(dt_bad)
    bad_match = DeviceTypeDB.get_db().find_matching_device_type(ld)
    DeviceTypeDB.get_db().add(dt)

    match = DeviceTypeDB.get_db().find_matching_device_type(ld)
    assert match[1].name == dt.name
    assert bad_match[0] < match[0] < 1.0
