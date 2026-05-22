from pathlib import Path
from pipeline.build_site import build_day_list_html, load_course_plan


def test_load_course_plan_returns_two_courses():
    plan = load_course_plan(Path("data/course-plan.json"))
    assert len(plan["kurse"]) == 2
    assert plan["kurse"][0]["id"] == "22_Bo_143"


def test_build_day_list_html_contains_all_days():
    plan = load_course_plan(Path("data/course-plan.json"))
    kurs = plan["kurse"][0]
    html = build_day_list_html(kurs)
    assert "<!DOCTYPE html>" in html
    assert kurs["titel"] in html
    for tag in kurs["tage"]:
        assert tag["datum"] in html
        assert tag["thema"] in html


def test_build_material_picker_includes_5_phases():
    from pipeline.build_site import build_material_picker_html, load_course_plan
    plan = load_course_plan()
    kurs = plan["kurse"][0]
    tag = kurs["tage"][0]
    html = build_material_picker_html(kurs, tag)
    assert "PRÄSENTATION" in html
    assert "QUIZ" in html
    assert "LERNPFAD" in html
    assert "quiz.html" in html
    assert "lernpfad.html" in html
    assert "praesentation.html" in html
