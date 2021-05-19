from scorm.scorm import jinja_template
def test_template():

    expected = """

"""

    dirName = ''
    htmlfile = ''
    all_resources = ''
    templatefile = ''

    actual = jinja_template(dirName, htmlfile, all_resources, templatefile)

    assert actual == expected