import json

from allotropy.parser_factory import Vendor
from allotropy.testing.utils import from_file

file_name = "softmaxpro_abs_endpoint_plates.txt"

# test_filepath = f"../tests/parsers/appbio_quantstudio/testdata/{file_name}"
# test_filepath = f"ab_quantstudio_test_data/{file_name}"
test_filepath = f"../../aurelia/packages/benchling-asm-parser/tests/plate_reader/testdata/{file_name}"

allotrope_dict = from_file(test_filepath, Vendor.MOLDEV_SOFTMAX_PRO)

print(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))  # noqa: T201
