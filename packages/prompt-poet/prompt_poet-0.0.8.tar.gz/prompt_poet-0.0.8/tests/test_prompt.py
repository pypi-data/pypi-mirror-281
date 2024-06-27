import os
import pytest
import jinja2 as j2
from prompt import Prompt
from examples.cai_helpers import CAIMessage

CWD = os.path.dirname(__file__)

def test_simple_prompt_sad():
    with pytest.raises(ValueError, match="`token_limit` is a reserved key in the template data."):
        _ = Prompt(
            template_data={"var1": "foobar", "token_limit": 10},
            template_name=os.path.abspath(
                os.path.join(CWD, "templates", "simple_prompt.yml.j2")
            ),
        )

    with pytest.raises(ValueError, match="`escape_special_characters` is a reserved key in the template data."):
        _ = Prompt(
            template_data={"var1": "foobar", "escape_special_characters": lambda x: x},
            template_name=os.path.abspath(
                os.path.join(CWD, "templates", "simple_prompt.yml.j2")
            ),
        )
    
def test_simple_prompt_happy():
    prompt = Prompt(
        template_data={"var1": "foobar"},
        template_name=os.path.abspath(
            os.path.join(CWD, "templates", "simple_prompt.yml.j2")
        ),
    )
    assert prompt.string == "Raw string of the first part foobar"

    prompt = Prompt(
        template_data={"var1": "foobar"},
        template_name="simple_prompt.yml.j2",
        template_dir=os.path.abspath(
            os.path.join(CWD, "templates"),
        ),
    )
    assert prompt.string == "Raw string of the first part foobar"

def test_section_prompt_happy():
    prompt = Prompt(
        template_data={"var1": "foobar"},
        template_name="section_prompt.yml.j2",
        template_dir=os.path.abspath(
            os.path.join(CWD, "templates"),
        ),
    )
    assert prompt.string == "Raw string of section_aRaw string of section_b"

def test_macros_prompt_happy():
    prompt = Prompt(
        template_data={"var1": "foobar"},
        template_name="macros_prompt.yml.j2",
        template_dir=os.path.abspath(
            os.path.join(CWD, "templates"),
        ),
    )
    assert prompt.string == "<|beginningofdialog|>Raw string of first part<|endofmessage|><|beginningofmessage|>Raw string of second part<|endofmessage|>"

def test_function_prompt_happy():
    prompt = Prompt(
        template_data={
            "var1": "foo",
            "var2": "bar",
            "concat_strings": lambda x, y: x + y,
        },
        template_name="function_prompt.yml.j2",
        template_dir=os.path.abspath(
            os.path.join(CWD, "templates"),
        ),
    )
    assert prompt.string == "foobar"

def test_template_not_found():
    with pytest.raises(j2.TemplateNotFound):
        _ = Prompt(
            template_data={"var1": "foobar"},
            template_name="non_existent_template.yml.j2",
            template_dir=os.path.abspath(
                os.path.join(CWD, "templates")
            ),

        )

def test_control_flow_happy():
    prompt = Prompt(
        template_data={"conditional": True},
        template_name="control_flow_prompt.yml.j2",
        template_dir=os.path.abspath(
            os.path.join(CWD, "templates"),
        ),
    )
    assert "Raw string of conditional" in prompt.string
    assert "Raw string of item" not in prompt.string

    prompt = Prompt(
        template_data={"conditional": False, "items": ["item1", "item2", "item3"]},
        template_name="control_flow_prompt.yml.j2",
        template_dir=os.path.abspath(
            os.path.join(CWD, "templates"),
        ),
    )
    assert "Raw string of conditional" not in prompt.string
    assert "Raw string of item item1" in prompt.string
    assert "Raw string of item item2" in prompt.string
    assert "Raw string of item item3" in prompt.string

    prompt = Prompt(
        template_data={"conditional": True, "items": ["item1", "item2", "item3"]},
        template_name="control_flow_prompt.yml.j2",
        template_dir=os.path.abspath(
            os.path.join(CWD, "templates"),
        ),
    )
    assert "Raw string of conditional" in prompt.string
    assert "Raw string of item item1" in prompt.string
    assert "Raw string of item item2" in prompt.string
    assert "Raw string of item item3" in prompt.string

def test_example_cai_template_happy():
    prompt = Prompt(
        template_data={
            "timestamp": "2024 06 24",
            "username": "Jeff", 
            "character": {
                "title": "The title",
                "description": "The description",
                "definition": "The definition\nWith multiple lines\nIn the definition",
                "participant__name": "Alice",
            },
            "persona_definition": "The persona definition",
            "cai_messages": [
                CAIMessage(author="Alice", text="The first message"),
                CAIMessage(author="Jeff", text="The second message"),
                CAIMessage(author="Alice", text="The third message", is_pinned=True),
                CAIMessage(author="Jeff", text="The fourth message"),
            ],
            "reply_prompt": "Alice:"
        },
        template_name="cai.yml.j2",
        from_examples=True,
        token_limit=100,
    )
    assert prompt.string == "<|beginningofdialog|>2024 06 24 Alice: The title - The description<|endofmessage|><|beginningofmessage|>narrator: The definition<|endofmessage|><|beginningofmessage|>narrator: With multiple lines<|endofmessage|><|beginningofmessage|>narrator: In the definition<|endofmessage|><|beginningofmessage|>Jeff: The persona definition<|endofmessage|><|beginningofmessage|>Alice: The third message<|endofmessage|><|beginningofmessage|>Alice: The first message<|endofmessage|><|beginningofmessage|>Jeff: The second message<|endofmessage|><|beginningofmessage|>Alice: The third message<|endofmessage|><|beginningofmessage|>Jeff: The fourth message<|endofmessage|><|beginningofmessage|>Alice:"

    # With escaped special characters.
    prompt = Prompt(
        template_data={
            "timestamp": "2024 06 24",
            "username": "Jeff", 
            "character": {
                "title": "The \r title",
                "description": "The description",
                "definition": "The definition\nWith multiple lines\nIn the definition",
                "participant__name": "Alice",
            },
            "persona_definition": "The persona \r definition",
            "cai_messages": [
                CAIMessage(author="Alice", text="The first \n \n message"),
                CAIMessage(author="Jeff", text="The second \r message"),
                CAIMessage(author="Alice", text="The third message", is_pinned=True),
                CAIMessage(author="Jeff", text="The fourth ' message"),
            ],
            "reply_prompt": "Alice:"
        },
        template_name="cai.yml.j2",
        from_examples=True,
        token_limit=100,
    )
    assert prompt.string == "<|beginningofdialog|>2024 06 24 Alice: The \r title - The description<|endofmessage|><|beginningofmessage|>narrator: The definition<|endofmessage|><|beginningofmessage|>narrator: With multiple lines<|endofmessage|><|beginningofmessage|>narrator: In the definition<|endofmessage|><|beginningofmessage|>Jeff: The persona \r definition<|endofmessage|><|beginningofmessage|>Alice: The third message<|endofmessage|><|beginningofmessage|>Alice: The first \n \n message<|endofmessage|><|beginningofmessage|>Jeff: The second \r message<|endofmessage|><|beginningofmessage|>Alice: The third message<|endofmessage|><|beginningofmessage|>Jeff: The fourth ' message<|endofmessage|><|beginningofmessage|>Alice:"
