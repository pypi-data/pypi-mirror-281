import datetime as dt

import smartsettings as ss


def test_SmartSettings():
    class A(ss.SmartSettings):
        def __init__(self, name, value) -> None:
            self.name = name
            self.value = value

    class B(ss.SmartSettings):
        def __init__(self, name, value) -> None:
            self.name = name
            self.value = value
            self.a_list = [
                {i: A(f"{self.name}'s A{i}", self.value * 10 + i)} for i in range(2)
            ]

    class C(ss.SmartSettings):
        def __init__(self, name, value) -> None:
            self.name = name
            self.value = value
            self.b_dict = {
                i: [B(f"{self.name}'s B{i}", self.value * 10 + i)] for i in range(2)
            }

    c0 = C("C0", 0)
    # print("c0")
    # print(c0.__dict__)
    # print()

    c1 = C("C1", 1)
    # print("c1")
    # print(c1.__dict__)
    # print()

    # Update c0 with c1
    c0 << c1
    # print("Updated c0")
    # print(c0.__dict__)
    # print()

    # After updating, all of the values of the attributes of c0 is the same as c1.
    # And all of the addresses of the attributes of c0 remain unchanged.

    # Test if all of the values in c0 are the same as c1
    assert c0.name == c1.name
    assert c0.value == c1.value

    for key in c0.b_dict:
        assert c0.b_dict[key][0].name == c1.b_dict[key][0].name
        assert c0.b_dict[key][0].value == c1.b_dict[key][0].value
        for i, item in enumerate(c0.b_dict[key][0].a_list):
            for k in item:
                assert (
                    c0.b_dict[key][0].a_list[i][k].name
                    == c1.b_dict[key][0].a_list[i][k].name
                )
                assert (
                    c0.b_dict[key][0].a_list[i][k].value
                    == c1.b_dict[key][0].a_list[i][k].value
                )

    # Test if all of the updatable objects in c0 are different from c1
    assert c0 is not c1

    for key in c0.b_dict:
        assert c0.b_dict[key][0] is not c1.b_dict[key][0]
        for i, item in enumerate(c0.b_dict[key][0].a_list):
            for k in item:
                assert (
                    c0.b_dict[key][0].a_list[i][k] is not c1.b_dict[key][0].a_list[i][k]
                )

    # When there is no `AssertionError`, it means the test is passed

    settings = ss.SmartSettings(
        name="Quan Lin",
        age=42,
        num=3.14,
        date=dt.datetime.now(dt.timezone.utc),
        _private=True,
    )
    settings.added_info1 = "This info is added afterward."
    settings["added_info2"] = 100
    settings["你好"] = "世界"
    print(settings)
    print(settings["added_info3"])

    settings_string = ss.to_string(
        settings,
        crypto_key="secret",
    )
    print(settings_string)

    new_settings = ss.from_string(
        settings_string,
        crypto_key="secret",
    )
    print(new_settings)
    print("Test if new_settings == settings:")
    print(new_settings == settings)

    loaded_settings = ss.from_file(
        "settings/settings.txt",
        crypto_key="secret",
        default_settings=settings,
    )
    print(loaded_settings)
    print("Test if loaded_settings == settings:")
    print(loaded_settings == settings)

    ss.to_file(
        loaded_settings,
        "settings/settings.txt",
        crypto_key="secret",
        backup_num=2,
    )

    print(settings.你好)
    print(settings["你好"])

    settings[" race car "] = "A nice race car."
    print(settings[" race car "])


if __name__ == "__main__":
    test_SmartSettings()
