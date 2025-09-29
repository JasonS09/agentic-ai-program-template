from src.prompt.templating import PromptTemplate, join_blocks


def test_prompt_template_basic():
    tpl = PromptTemplate("Hello ${name}")
    assert tpl.render({"name": "World"}) == "Hello World"


def test_required_variables():
    tpl = PromptTemplate("A ${x} and ${y}")
    vars_ = tpl.required_variables()
    assert {"x", "y"}.issubset(vars_)


def test_join_blocks_skips_empty():
    result = join_blocks("One", " ", "Two", "")
    assert result == "One\n\nTwo"
