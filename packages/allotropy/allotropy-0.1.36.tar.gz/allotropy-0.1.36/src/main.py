import json

from allotropy.parser_factory import Vendor
from allotropy.to_allotrope import allotrope_from_file

if __name__ == "__main__":
    for output_file in (
        "appbio_quantstudio_test05.txt",
        # "appbio_quantstudio_test06.txt",
    ):
        test_filepath = (
            f"../tests/parsers/appbio_quantstudio/testdata/{output_file}"
            # f"../../aurelia/packages/benchling-asm-parser/tests/polymerase_chain_reaction/testdata/{output_file}"
        )
        allotrope_dict = allotrope_from_file(test_filepath, Vendor.APPBIO_QUANTSTUDIO)
        print(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))  # noqa: T201
