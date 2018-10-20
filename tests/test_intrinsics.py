import pytest

from samtranslator.model.intrinsics import is_instrinsic, make_shorthand

class TestIntrinsics(object):

    @pytest.mark.parametrize("intrinsic_name", [
        "Ref",
        "Condition",
        "Fn::foo",
        "Fn::sub",
        "Fn::something"
    ])
    def test_is_intrinsic_must_detect_intrinsics(self, intrinsic_name):

        indict = {
            intrinsic_name: intrinsic_name
        }

        assert is_instrinsic(indict)

    def test_is_intrinsic_on_empty_input(self):
        assert not is_instrinsic(None)

    def test_is_intrinsic_on_non_dict_input(self):
        assert not is_instrinsic([1,2,3])

    def test_is_intrinsic_on_intrinsic_like_dict_input(self):
        assert not is_instrinsic({
            "Ref": "foo",
            "key": "bar"
        })

    @pytest.mark.parametrize("input, expected", [
        ({"Ref": "foo"}, "${foo}"),
        ({"Fn::GetAtt": ["foo", "Arn"]}, "${foo.Arn}")
    ])
    def test_make_shorthand_success(self, input, expected):
        assert make_shorthand(input) == expected

    def test_make_short_hand_failure(self):
        input = { "Fn::Sub": "something" }

        with pytest.raises(NotImplementedError):
            make_shorthand(input)
