from typing import Union
from scipy.spatial import ConvexHull
from shapely import Polygon
from pydantic import BaseModel, conlist, Field as dataclass_field
from moapy.auto_convert import auto_schema

from sectionproperties.pre.library.concrete_sections import add_bar
from concreteproperties.concrete_section import ConcreteSection
from concreteproperties.material import Concrete, SteelBar

import sectionproperties.pre.geometry as geometry
import sectionproperties.pre.pre as pre
import concreteproperties.stress_strain_profile as ssp
import concreteproperties.utils as utils
import concreteproperties.results
import numpy as np
import trimesh
import pandas as pd
# ==== Unit & Design Code ====

class Res3DPM(BaseModel):
    """
    3DPM result class
    """
    HEAD: conlist(str, min_length=3, max_length=3) = dataclass_field(default=["Mx", "My", "P"])
    DATA: list[conlist(float, min_length=3, max_length=3)] = dataclass_field(default=[[0.0, 0.0, 0.0]])

    class Config:
        title = "3DPM Result"

    def to_dict(self):
        return [dict(zip(self.HEAD, row)) for row in self.DATA]

class ResStrength(BaseModel):
    """
    Strength result class
    """
    HEAD: conlist(str, min_length=4, max_length=4) = dataclass_field(default=["Name", "Mny", "Mnz", "Pn"])
    DATA: list[conlist(Union[str, float], min_length=4, max_length=4)] = dataclass_field(default=None)

    class Config:
        title = "Strength Result"

    def to_dict(self):
        return [dict(zip(self.HEAD, row)) for row in self.DATA]

class gsd3dpmResult(BaseModel):
    """
    Section Property
    {
        "HEAD": ["Area", "Asy", "Asz", "Ixx", "Iyy", "Izz", "Cy", "Cz", "Syp", "Sym", "Szp", "Szm", "Ipyy", "Ipzz", "Zy", "Zz", "ry", "rz"]
        "DATA": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0]
    }
    """
    PM_Curve: Res3DPM = dataclass_field(default=Res3DPM())
    Strength: ResStrength = dataclass_field(default=ResStrength())

    class Config:
        title = "Section Property"

class gsdUnit(BaseModel):
    """
    GSD global unit class
    """
    force: str = dataclass_field(
        default="kN", description="Force unit")
    length: str = dataclass_field(
        default="m", description="Length unit")
    section_dimension: str = dataclass_field(
        default="mm", description="Section dimension unit")
    pressure: str = dataclass_field(
        default="MPa", description="Pressure unit")
    strain: str = dataclass_field(
        default="%", description="Strain unit")

    class Config:
        title = "GSD Unit"

class gsdDesignCode(BaseModel):
    design_code: str = dataclass_field(default="ACI 318-19", max_length=30)
    sub_code: str = dataclass_field(default="SI")

    class Config:
        title = "GSD Design Code"


# ==== Stress Strain Curve ====
class stress_strain_curve(BaseModel):
    """
    Stress strain curve class
    {
        "HEAD": ["Strain", "Stress"],
        "DATA": [[0.1, 2, 4, 4, 35], [0, 234235, 235, 235, 0]],
    }
    """
    HEAD: conlist(str, min_length=2, max_length=2)
    DATA: conlist(list[float], min_length=2, max_length=2)

    class Config:
        title = "Stress Strain Curve"


# ==== Concrete Material ====
class gsdConcreteGrade(BaseModel):
    """
    GSD concrete class
    """
    design_code: str = dataclass_field(
        default="ACI318M-19", description="Design code")
    grade: str = dataclass_field(
        default="C12", description="Grade of the concrete")

    class Config:
        title = "GSD Concrete Grade"

class concrete_general_properties(BaseModel):
    """
    GSD concrete general properties for calculation
    """
    strength: int = dataclass_field(
        gt=0, default=12, description="Grade of the concrete")
    elastic_modulus: float = dataclass_field(
        gt=0, default=30000, description="Elastic modulus of the concrete")
    density: float = dataclass_field(
        gt=0, default=2400, description="Density of the concrete")
    thermal_expansion_coefficient: float = dataclass_field(
        gt=0, default=0.00001, description="Thermal expansion coefficient of the concrete")
    poisson_ratio: float = dataclass_field(
        gt=0, default=0.2, description="Poisson ratio of the concrete")

    class Config:
        title = "GSD Concrete General Properties"

class concrete_stress_uls_options_ACI(BaseModel):
    """
    GSD concrete stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Rectangle", description="Material model for ULS")
    factor_b1: float = dataclass_field(
        default=0.85, description="Plastic strain limit for ULS")
    compressive_failure_strain: float = dataclass_field(
        default=0.003, description="Failure strain limit for ULS")

    class Config:
        title = "GSD Concrete Stress Options for ULS"

class concrete_stress_uls_options_Eurocode(BaseModel):
    """
    GSD concrete stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Rectangle", description="Material model for ULS")
    partial_factor_case: float = dataclass_field(
        default=1.0, description="Partial factor case for ULS")
    partial_factor: float = dataclass_field(
        default=1.5, description="Partial factor for ULS")
    compressive_failure_strain: float = dataclass_field(
        default=0.003, description="Failure strain limit for ULS")

    class Config:
        title = "GSD Concrete Stress Options for ULS"

class concrete_sls_options(BaseModel):
    """
    GSD concrete stress options for SLS
    """
    material_model: str = dataclass_field(
        default="Linear", description="Material model for SLS")
    plastic_strain_limit: float = dataclass_field(
        default=0.002, description="Plastic strain limit for SLS")
    failure_compression_limit: float = dataclass_field(
        default=0.003, description="Failure compression limit for SLS")
    material_model_tension: str = dataclass_field(
        default="interpolated", description="Material model for SLS tension")
    failure_tension_limit: float = dataclass_field(
        default=0.003, description="Failure tension limit for SLS")

    class Config:
        title = "GSD Concrete Stress Options for SLS"

# ==== Rebar Materials ====
class gsdRebarGrade(BaseModel):
    """
    GSD rebar grade class
    """
    design_code: str = dataclass_field(
        default="ACI318M-19", description="Design code")
    grade: str = dataclass_field(
        default="Grade 420", description="Grade of the rebar")

    class Config:
        title = "GSD Rebar Grade"

class gsdRebarProp(BaseModel):
    """
    GSD rebar prop
    """
    area: float = dataclass_field(
        default=287.0, description="Area of the rebar")
    material: gsdRebarGrade = dataclass_field(
        default=gsdRebarGrade(), description="Material of the rebar")

    class Config:
        title = "GSD Rebar Properties"

class rebar_general_properties(BaseModel):
    """
    GSD rebar general properties for calculation
    """
    strength: int = dataclass_field(
        default=420, description="Grade of the rebar")
    elastic_modulus: float = dataclass_field(
        default=200000, description="Elastic modulus of the rebar")
    density: float = dataclass_field(
        default=7850, description="Density of the rebar")
    thermal_expansion_coefficient: float = dataclass_field(
        default=0.00001, description="Thermal expansion coefficient of the rebar")
    poisson_ratio: float = dataclass_field(
        default=0.3, description="Poisson ratio of the rebar")

    class Config:
        title = "GSD Rebar General Properties"

class rebar_stress_uls_options_ACI(BaseModel):
    """
    GSD rebar stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", description="Material model for ULS")
    failure_strain: float = dataclass_field(
        default=0.7, description="Failure strain limit for ULS")

    class Config:
        title = "GSD Rebar Stress Options for ULS"

class rebar_stress_sls_options(BaseModel):
    """
    GSD rebar stress options for SLS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", description="Material model for SLS")
    failure_strain: float = dataclass_field(
        default=0.7, metadata={"default" : 0.7, "description": "Failure strain limit for SLS"})

    class Config:
        title = "GSD Rebar Stress Options for SLS"

class gsdMaterialRebar(BaseModel):
    """
    GSD rebar class
    """
    grade: gsdRebarGrade = dataclass_field(
        default=gsdRebarGrade(), description="Grade of the rebar")
    curve_uls: stress_strain_curve = dataclass_field(
        default=stress_strain_curve(HEAD=["Strain", "Stress"],
                                    DATA=[[0.0, 0.0025, 0.05], [0, 500.0, 500.0]]), description="Stress strain curve")
    curve_sls: stress_strain_curve = dataclass_field(
        default=stress_strain_curve(HEAD=["Strain", "Stress"],
                                    DATA=[[0.0, 0.0025, 0.05], [0, 500.0, 500.0]]), description="Stress strain curve")

    class Config:
        title = "GSD Material Rebar"

class gsdMaterialTendon(BaseModel):
    """
    GSD tendon class
    """
    code: str = dataclass_field(
        default="ASTM A416", description="Tendon code")
    curve_uls: stress_strain_curve = dataclass_field(
        default=None, description="Stress strain curve")
    curve_sls: stress_strain_curve = dataclass_field(
        default=None, description="Stress strain curve")

class gsdMaterialConcrete(BaseModel):
    """
    GSD material for Concrete class
    """
    grade: gsdConcreteGrade = dataclass_field(
        default=gsdConcreteGrade(), description="Grade of the concrete")
    curve_uls: stress_strain_curve = dataclass_field(
        default=stress_strain_curve(HEAD=["Strain", "Stress"],
                                    DATA=[[0.0, 0.0006, 0.0006, 0.003], [0.0, 0.0, 34.0, 34.0]]), description="Stress strain curve")
    curve_sls: stress_strain_curve = dataclass_field(
        default=stress_strain_curve(HEAD=["Strain", "Stress"],
                                    DATA=[[0.0, 0.001], [0, 32.8,]]), description="Stress strain curve")

    class Config:
        title = "GSD Material Concrete"

class gsdMaterial(BaseModel):
    """
    GSD concrete class
    """
    concrete: gsdMaterialConcrete = dataclass_field(
        default=gsdMaterialConcrete(), description="Concrete properties")
    rebar: gsdMaterialRebar = dataclass_field(
        default=gsdMaterialRebar(), description="Rebar properties")
    tendon: gsdMaterialTendon = dataclass_field(
        default=None, description="Tendon properties")

    class Config:
        title = "GSD Material"

# ==== Geometry ====
class gsdPoints(BaseModel):
    """
    GSD Points class
    "HEAD": ["x", "y"],
    "DATA": [[0.0, 400.0, 400.0, 0.0], [0.0, 0.0, 600.0, 600.0]],
    """
    HEAD: conlist(str, min_length=2, max_length=2)
    DATA: conlist(list[float], min_length=2, max_length=2)

    class Config:
        title = "GSD Points"

class gsdConcreteGeometry(BaseModel):
    """
    GSD concrete geometry class
    """
    outerPolygon: gsdPoints = dataclass_field(
        default=gsdPoints(HEAD=["x", "y"],
                          DATA=[[0.0, 400.0, 400.0, 0.0], [0.0, 0.0, 600.0, 600.0]]), description="Outer polygon of the concrete")
    innerPolygon: gsdPoints = dataclass_field(
        default=None, description="Inner polygon of the concrete")
    material: gsdConcreteGrade = dataclass_field(
        default=gsdConcreteGrade(), description="Material of the concrete")

    class Config:
        title = "GSD Concrete Geometry"

class gsdRebarGeometry(BaseModel):
    """
    GSD rebar geometry class
    """
    position: gsdPoints = dataclass_field(
        default=gsdPoints(HEAD=["x", "y"],
                          DATA=[[40.0, 360.0, 360.0, 40.0], [40.0, 40.0, 560.0, 560.0]]), description="position of the rebar")
    prop: gsdRebarProp = dataclass_field(
        default=gsdRebarProp(), description="properties of the rebar")

    class Config:
        title = "GSD Rebar Geometry"

class gsdGeometry(BaseModel):
    """
    GSD geometry class
    """
    concrete: gsdConcreteGeometry = dataclass_field(
        default=gsdConcreteGeometry(), description="Concrete geometry")
    rebar: gsdRebarGeometry = dataclass_field(
        default=gsdRebarGeometry(), description="Rebar geometry")

    class Config:
        title = "GSD Geometry"

# ==== Load ====
class loadcomb(BaseModel):
    """
    GSD load comb class
    "HEAD": ["Name", "Fx", "My", "Mz"],
    "DATA": [["1", 100, 10, 10], ["2", 200, 10, 20]],
    """
    HEAD: conlist(str, min_length=4, max_length=4)
    DATA: list[conlist(Union[str, float], min_length=4, max_length=4)]

    class Config:
        title = "GSD Load Combination"

class gsdLcb(BaseModel):
    """
    GSD load combination class
    """
    uls: loadcomb = dataclass_field(
        default=loadcomb(HEAD=["name", "Fx", "My", "Mz"],
                         DATA=[["uls1", 100.0, 10.0, 50.0], ["uls2", 100.0, 15.0, 50.0]]), description="uls load combination")
    sls: loadcomb = dataclass_field(
        default=loadcomb(HEAD=["name", "Fx", "My", "Mz"],
                         DATA=[["sls1", 100.0, 10.0, 50.0], ["sls2", 100.0, 15.0, 50.0]]), description="sls load combination")

    class Config:
        title = "GSD Load Combination"

# ==== options ====
class gsdOptions(BaseModel):
    """
    GSD options class
    """
    by_ecc_pu: str = dataclass_field(
        default="ecc", description="ecc or P-U")

    class Config:
        title = "GSD Options"


# ==== functions ====
@auto_schema
def conc_properties_design(
    general: concrete_general_properties,
    uls: concrete_stress_uls_options_ACI,
    sls: concrete_sls_options
) -> dict[str, stress_strain_curve]:
    """
    Return the concrete material properties based on the design code

    Args:
        general: general concrete properties
        uls: concrete stress options for ULS
        sls: concrete stress options for SLS

    return:
        { "ULS": "strain":[0.1,2,4,4,35,], "stress":[0,234235,235,235,], "SLS": stress_strain_curve }: material properties of selected data
    """
    if general is None:
        general = concrete_general_properties()
    if uls is None:
        uls = concrete_stress_uls_options_ACI()
    if sls is None:
        sls = concrete_sls_options()

    if uls.material_model == 'Rectangle':
        _uls_strains = [
            0,
            uls.compressive_failure_strain * (1 - uls.factor_b1),
            uls.compressive_failure_strain * (1 - uls.factor_b1),
            uls.compressive_failure_strain,
        ]
        _uls_stress = [
            0,
            0,
            uls.factor_b1 * general.strength,
            uls.factor_b1 * general.strength,
        ]

    if sls.material_model == 'Linear':
        _sls_strains = [
            0,
            sls.failure_compression_limit,
        ]
        _sls_stress = [
            0,
            general.strength,
        ]

    return {
        "ULS": stress_strain_curve(HEAD=["Strain", "Stress"], DATA=[_uls_strains, _uls_stress]).dict(),
        "SLS": stress_strain_curve(HEAD=["Strain", "Stress"], DATA=[_sls_strains, _sls_stress]).dict(),
    }

@auto_schema
def rebar_properties_design(
    general: rebar_general_properties,
    uls: rebar_stress_uls_options_ACI,
    sls: rebar_stress_sls_options
) -> dict[str, stress_strain_curve]:
    """
    Return the material properties based on the design code

    Args:
        general: general rebar properties
        uls: rebar stress options for ULS
        sls: rebar stress options for SLS

    return:
        { "ULS": "strain":[0.1,2,4,4,35,], "stress":[0,234235,235,235,], "SLS": stress_strain_curve }: material properties of selected data
    """
    yield_strain = general.strength / general.elastic_modulus

    _sls_strains = [
        0,
        yield_strain,
        sls.failure_strain
    ]
    _sls_stress = [
        0,
        general.strength
    ]

    _uls_strains = [
        0,
        yield_strain,
        uls.failure_strain
    ]
    _uls_stress = [
        0,
        general.strength
    ]

    print(_sls_strains)
    print(_uls_strains)

    return {
        "ULS": stress_strain_curve(HEAD=["Strain", "Stress"], DATA=[_uls_strains, _uls_stress]).dict(),
        "SLS": stress_strain_curve(HEAD=["Strain", "Stress"], DATA=[_sls_strains, _sls_stress]).dict(),
    }

class PM3DCurve:
    """
    Class for PM3D Curve Calculation
    """
    def __init__(self, matl=gsdMaterial, geom=gsdGeometry, lcb=gsdLcb, opt=gsdOptions):
        if hasattr(matl, "concrete"):
            self.conc = matl.concrete
            if self.conc is not None:
                self.concrete_material_uls = self.conc.curve_uls
                self.concrete_material_sls = self.conc.curve_sls

        if hasattr(matl, "rebar"):
            self.rebar = matl.rebar
            if self.rebar is not None:
                self.rebar_material_uls = self.rebar.curve_uls
                self.rebar_material_sls = self.rebar.curve_sls

        self.geom = geom
        if self.geom is not None:
            self.concrete_geom = self.geom.concrete
            self.rebar_geom = self.geom.rebar

        self.lcom = lcb
        if self.lcom is not None:
            self.lcom_uls = self.lcom.uls
            self.lcom_sls = self.lcom.sls

        self.option = opt

    def get_concrete_material_curve(self, type_):
        if type_ == "uls":
            curve_data = self.concrete_material_uls
        elif type_ == "sls":
            curve_data = self.concrete_material_sls

        head = curve_data.HEAD
        data = curve_data.DATA
        if head and data:
            strain = data[0]
            stress = data[1]
            return {"Strain": strain, "Stress": stress}
        return {}

    def get_rebar_material_curve(self, type_):
        if type_ == "uls":
            curve_data = self.rebar_material_uls
        elif type_ == "sls":
            curve_data = self.rebar_material_sls

        head = curve_data.HEAD
        data = curve_data.DATA
        if head and data:
            strain = data[0]
            stress = data[1]
            return {"Strain": strain, "Stress": stress}
        return {}

    def get_max_strain_with_zero_stress(self, data):
        df = pd.DataFrame(data["DATA"]).transpose()
        df.columns = data["HEAD"]

        zero_stress_strains = df[df["Stress"] == 0.0]["Strain"]

        max_strain = zero_stress_strains.max()
        return max_strain

    def get_concrete_geom(self):
        return self.concrete_geom

    def get_rebar_geom(self):
        return self.rebar_geom

    def get_lcom_uls_data(self):
        return self.lcom_uls.DATA

    def get_lcom_sls_data(self):
        return self.lcom_sls.DATA

    def get_option_by_ecc_pu(self):
        return self.option.by_ecc_pu

    def compound_section(
        self,
        concrete: list[dict],
        rebar: list[dict],
        conc_mat: pre.Material = pre.DEFAULT_MATERIAL,
        steel_mat: pre.Material = pre.DEFAULT_MATERIAL,
    ) -> geometry.CompoundGeometry:
        conc_polygon = concrete.outerPolygon
        coords = conc_polygon.DATA

        def convert_data(data):
            x_coords = data[0]
            y_coords = data[1]

            if len(x_coords) != len(y_coords):
                raise ValueError("The length of x and y coordinates must be the same.")

            # Create tuples of (x, y)
            result = [(x_coords[i], y_coords[i]) for i in range(len(x_coords))]

            return result

        polygon = Polygon(convert_data(coords))
        concrete_geometry = geometry.Geometry(geom=polygon, material=conc_mat)
        area = rebar.prop.area
        posi = rebar.position.DATA
        trans_pos = convert_data(posi)

        for x, y in trans_pos:
            concrete_geometry = add_bar(
                geometry=concrete_geometry,
                area=area,
                material=steel_mat,
                x=x,
                y=y,
                n=4
            )

        if isinstance(concrete_geometry, geometry.CompoundGeometry):
            return concrete_geometry
        else:
            raise ValueError("Concrete section generation failed.")

    def get_Cb(self, sect, theta_rad, ecu, esu):
        d_ext, _ = sect.extreme_bar(theta=theta_rad)
        return (ecu / (ecu + esu)) * d_ext

    def make_3dpm_data(self):
        if self.conc is None or self.rebar is None or self.geom is None or self.lcom is None:
            return "Data is not enough."

        beta1 = 0.8
        ecu = 0.003
        esu = 0.05
        fck = 30.0

        ss_conc_uls = ssp.ConcreteUltimateProfile(self.get_concrete_material_curve("uls")["Strain"], self.get_concrete_material_curve("uls")["Stress"], fck)
        ss_conc_ser = ssp.ConcreteServiceProfile(self.get_concrete_material_curve("sls")["Strain"], self.get_concrete_material_curve("sls")["Stress"], ecu)

        # ss_rebar_uls = ssp.StressStrainProfile(self.get_rebar_material_curve("uls")["Strain"], self.get_rebar_material_curve("uls")["Stress"])
        # ss_rebar_sls = ssp.StressStrainProfile(self.get_rebar_material_curve("sls")["Strain"], self.get_rebar_material_curve("sls")["Stress"])

        concrete_matl = Concrete(
            name=self.conc.grade.grade,
            density=2.4e-6,
            stress_strain_profile=ss_conc_ser,
            ultimate_stress_strain_profile=ss_conc_uls,
            flexural_tensile_strength=0.6 * np.sqrt(40),
            colour="lightgrey",
        )

        steel_matl = SteelBar(
            name=self.rebar.grade.grade,
            density=7.85e-6,
            stress_strain_profile=ssp.SteelElasticPlastic(
                yield_strength=500,
                elastic_modulus=200e3,
                fracture_strain=esu,
            ),
            colour="grey",
        )

        # reference geometry
        compound_sect = self.compound_section(self.get_concrete_geom(), self.get_rebar_geom(), concrete_matl, steel_matl)
        ref_sec = ConcreteSection(compound_sect)
        results = []
        theta_range = np.arange(0.0, 361.0, 15.0).tolist()

        for theta in theta_range:
            theta_rad = np.radians(theta)
            x11_max, x11_min, y22_max, y22_min = utils.calculate_local_extents( 
                geometry=ref_sec.compound_geometry,
                cx=ref_sec.gross_properties.cx,
                cy=ref_sec.gross_properties.cy,
                theta=theta_rad
            )

            C_Max = abs(y22_max - y22_min) / beta1
            d_n_range = np.linspace(0.0001, C_Max * 1.01, 10).tolist()  # numpy 배열을 float 리스트로 변환

            Cb = self.get_Cb(ref_sec, theta_rad, ecu, esu)
            d_n_range.append(Cb)

            for d_n in d_n_range:
                res = concreteproperties.results.UltimateBendingResults(theta_rad)
                res = ref_sec.calculate_ultimate_section_actions(d_n, res)
                results.append(res)

        return results

@auto_schema
def concrete_geometry(Polygon: gsdPoints, matl: gsdConcreteGrade) -> gsdConcreteGeometry:
    return gsdConcreteGeometry(outerPolygon=Polygon, material=matl)

@auto_schema
def calc_3dpm(
    material: gsdMaterial, geometry: gsdGeometry, lcb: gsdLcb, opt: gsdOptions
) -> gsd3dpmResult:
    """
    Return the 3D PM Curve & norminal strength points

    Args:
        material: gsdMaterial
        geometry: gsdGeometry
        lcb: gsdLcb
        opt: gsdOptions

    return:
        dict: 3DPM curve & norminal strength points about lcom
    """
    pm = PM3DCurve(material, geometry, lcb, opt)
    results = pm.make_3dpm_data()

    d_n_values = [result.n for result in results]
    m_x_values = [result.m_x for result in results]
    m_y_values = [result.m_y for result in results]

    points = np.column_stack((m_x_values, m_y_values, d_n_values))
    hull = ConvexHull(points)
    mesh1 = trimesh.Trimesh(vertices=hull.points, faces=hull.simplices)
    ray = trimesh.ray.ray_pyembree.RayMeshIntersector(mesh1)

    lcoms_uls = lcb.uls.DATA
    result_lcom_uls = []
    for lcom in lcoms_uls:
        lcom_name = lcom[0]
        lcom_point = [lcom[1], lcom[2], lcom[3]]

        if pm.get_option_by_ecc_pu() == "ecc":
            origin = np.array([0, 0, 0])
        else:
            origin = np.array([0, 0, lcom_point[2]])

        direction = lcom_point - origin
        direction = direction / np.linalg.norm(direction)

        locations, index_ray, index_tri = ray.intersects_location(
            ray_origins=np.array([origin]),
            ray_directions=np.array([direction])
        )

        result_lcom_uls.append([lcom_name, locations[0, 2], locations[0, 0], locations[0, 1]])

    hull_points_list = hull.points.tolist() if isinstance(hull.points, np.ndarray) else hull.points
    PM = Res3DPM(HEAD=["Mx", "My", "P"], DATA=hull_points_list)
    LcomRes = ResStrength(HEAD=["Name", "Mny", "Mnz", "Pn"], DATA=result_lcom_uls)
    return gsd3dpmResult(PM_Curve=PM, Strength=LcomRes)
