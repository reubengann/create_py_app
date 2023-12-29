from create_py_app.pick.picker import MultiOptionsPicker, SingleItemPicker


def pick_multi(options: list[tuple[str, bool]], title: str):
    picker = MultiOptionsPicker(options, title)
    return picker.start()


def pick_single(options: list[str], title: str) -> str:
    picker = SingleItemPicker(options, title)
    val = picker.start()
    assert val is not None
    return val[0]
