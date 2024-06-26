import pytest
import moapy.project.wgsd.wgsd_flow as wgsd_flow

def test_3dpm():
    material = wgsd_flow.gsdMaterial()
    material.concrete = wgsd_flow.gsdMaterialConcrete()
    material.concrete.grade = wgsd_flow.gsdConcreteGrade()
    material.concrete.curve_uls = wgsd_flow.stress_strain_curve(
        HEAD = ["Strain", "Stress"],
        DATA = [[0.0, 0.0006, 0.0006, 0.003], [0.0, 0.0, 34.0, 34.0]])
    material.concrete.curve_sls = wgsd_flow.stress_strain_curve(
        HEAD = ["Strain", "Stress"],
        DATA = [[0.0, 0.001], [0, 32.8,]])
    material.rebar = wgsd_flow.gsdMaterialRebar()
    material.rebar.grade = wgsd_flow.gsdRebarGrade()
    material.rebar.curve_uls = wgsd_flow.stress_strain_curve(
        HEAD = ["Strain", "Stress"],
        DATA = [[0.0, 0.0025, 0.05], [0, 500.0, 500.0]])
    material.rebar.curve_sls = wgsd_flow.stress_strain_curve(
        HEAD = ["Strain", "Stress"],
        DATA = [[0.0, 0.0025, 0.05], [0, 500.0, 500.0]])

    geom = wgsd_flow.gsdGeometry
    geom.concrete = wgsd_flow.gsdConcreteGeometry()
    geom.concrete.outerPolygon = wgsd_flow.gsdPoints(
        HEAD = ["x", "y"],
        DATA = [[0.0, 400.0, 400.0, 0.0], [0.0, 0.0, 600.0, 600.0]])
    geom.concrete.material = wgsd_flow.gsdConcreteGrade()

    reb = wgsd_flow.gsdRebarGeometry
    reb.prop = wgsd_flow.gsdRebarProp()
    reb.prop.area = 287.0
    reb.prop.material = wgsd_flow.gsdRebarGrade()
    reb.prop.material.grade = "Grade 420"
    reb.position = wgsd_flow.gsdPoints(
        HEAD = ["x", "y"],
        DATA = [[40.0, 360.0, 360.0, 40.0], [40.0, 40.0, 560.0, 560.0]])
    geom.rebar = reb

    lcb = wgsd_flow.gsdLcb
    lcb.uls = wgsd_flow.loadcomb(
        HEAD = ["name", "Fx", "My", "Mz"],
        DATA = [["uls1", 100.0, 10.0, 50.0], ["uls2", 100.0, 15.0, 50.0]])

    lcb.sls = wgsd_flow.loadcomb(
        HEAD = ["name", "Fx", "My", "Mz"],
        DATA = [["sls1", 100.0, 10.0, 50.0], ["sls2", 100.0, 15.0, 50.0]])
    opt = wgsd_flow.gsdOptions()
    res = wgsd_flow.calc_3dpm(material, geom, lcb, opt)
    data = res.Strength.to_dict()
    assert pytest.approx(data[0]['Name']) == 'uls1'
    assert pytest.approx(data[0]['Mny']) == 8520335.131574098
    assert pytest.approx(data[0]['Mnz']) == 17040670.263148196
    assert pytest.approx(data[0]['Pn']) == 1704067.0263148195
    assert pytest.approx(data[1]['Name']) == 'uls2'
    assert pytest.approx(data[1]['Mny']) == 8520335.131574098
    assert pytest.approx(data[1]['Mnz']) == 17040670.263148196
    assert pytest.approx(data[1]['Pn']) == 2556100.5394722293
