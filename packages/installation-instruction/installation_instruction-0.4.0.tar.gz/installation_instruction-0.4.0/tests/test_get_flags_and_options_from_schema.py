# Copyright 2024 Adam McKellar, Kanushka Gupta, Timo Ege

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from installation_instruction.get_flags_and_options_from_schema import _get_flags_and_options

def test_get_flags_and_options(test_data_flags_options):
    example_schema = test_data_flags_options
    options = _get_flags_and_options(example_schema, {"description": { "verbose": "Activate verbose output." }})

    assert len(options) == 6

    assert options[0].opts == ["--os"]
    assert options[0].help == "The operating system in which the package is installed."
    assert options[0].required == True
    assert options[0].default == None

    assert options[1].opts == ["--packager"]
    assert options[1].help == "The package manager of your choosing."
    assert options[1].required == False
    assert options[1].default == "pip"

    assert options[2].opts == ["--virtualenv"]
    assert options[2].help == "Choose if you want to use a virtual environment to install the package."
    assert options[2].required == False
    assert options[2].default == False

    assert options[3].opts == ["--compute-platform"]
    assert options[3].help == "Should your gpu or your cpu handle the task?"
    assert options[3].required == False
    assert options[3].default == "cu118"

    assert options[4].opts == ["--verbose"]
    assert options[4].help == "Activate verbose output."
    assert options[4].required == False
    assert options[4].default == False

    assert options[5].opts == ["--requiered-flag"]
    assert options[5].required == True
    assert options[5].default == None
