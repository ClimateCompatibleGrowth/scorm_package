from scorm_package.scorm import render_template, resourcelist
import os

def test_template_render_organisations():

    expected = """
<organizations default="lecture_block_1_organization">
  <organization identifier="lecture_block_1_organization">
  <title>Lecture Block 1</title>
    <item identifier="item_1" identifierref="lecture_1_1" isvisible="true">
      <title>Mini Lecture 1.1</title>
    </item>
    <item identifier="item_2" identifierref="lecture_1_2" isvisible="true">
      <title>Mini Lecture 1.2</title>
    </item>
  </organization>
</organizations>
"""

    block = '1'
    all_resources = ['res/Lecture_1.1.html', 'res/Lecture_1.2.html']
    templatefile = """
<organizations default="lecture_block_{{block}}_organization">
  <organization identifier="lecture_block_{{block}}_organization">
  <title>Lecture Block {{block}}</title>{% for resource in resourcelist %}
    <item identifier="item_{{loop.index}}" identifierref="lecture_{{block}}_{{loop.index}}" isvisible="true">
      <title>Mini Lecture {{block}}.{{loop.index}}</title>
    </item>{% endfor %}
  </organization>
</organizations>

"""

    actual = render_template(templatefile, all_resources, block)

    assert actual == expected

def test_template_render_resources():

    expected = """
<resources>
  <resource identifier="lecture_1_1" type="webcontent" adlcp:scormtype="sco" href="res/Lecture_1.1.html">
    <file href="res/Lecture_1.1.html"/>
  </resource>
  <resource identifier="lecture_1_2" type="webcontent" adlcp:scormtype="sco" href="res/Lecture_1.2.html">
    <file href="res/Lecture_1.2.html"/>
  </resource>
</resources>
"""

    template = """
<resources>{% for resource in resourcelist %}
  <resource identifier="lecture_{{block}}_{{loop.index}}" type="webcontent" adlcp:scormtype="sco" href="{{resource}}">
    <file href="{{resource}}"/>
  </resource>{% endfor %}
</resources>

"""

    block = '1'
    all_resources = ['res/Lecture_1.1.html', 'res/Lecture_1.2.html']
    actual = render_template(template, all_resources, block)

    assert actual == expected

def test_resource_list():

    actual = resourcelist(os.path.join('tests', 'fixtures', 'resourcelist'))
    expected = ['res/1.html', 'res/2.html', 'res/3.html']
    assert actual == expected