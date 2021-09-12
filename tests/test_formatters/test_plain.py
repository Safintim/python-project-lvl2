from gendiff.formatters.plain import get_current_path


def test_get_current_path():
    assert get_current_path('', 'common') == 'common'
    assert get_current_path('common', 'group') == 'common.group'
    assert get_current_path('common.setting', 'rk') == 'common.setting.rk'
