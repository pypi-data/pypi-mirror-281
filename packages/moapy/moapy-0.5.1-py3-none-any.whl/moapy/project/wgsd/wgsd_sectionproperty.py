from pydantic import BaseModel, conlist, Field as dataclass_field
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Polygon, Geometry
from moapy.auto_convert import auto_schema
from moapy.project.wgsd.wgsd_flow import gsdPoints
from moapy.mdreporter import ReportUtil, enUnit

class MSectionProperty(BaseModel):
    """
    Section Property
    {
        "HEAD": ["Area", "Asy", "Asz", "Ixx", "Iyy", "Izz", "Cy", "Cz", "Syp", "Sym", "Szp", "Szm", "Ipyy", "Ipzz", "Zy", "Zz", "ry", "rz"]
        "DATA": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0]
    }
    """
    HEAD: conlist(str, min_length=18, max_length=18) = dataclass_field(default=["Area", "Asy", "Asz", "Ixx", "Iyy", "Izz", "Cy", "Cz", "Syp", "Sym", "Szp", "Szm", "Ipyy", "Ipzz", "Zy", "Zz", "ry", "rz"])
    DATA: conlist(float, min_length=18, max_length=18) = dataclass_field(default=[10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0])

    class Config:
        title = "Section Property"

    def to_dict(self):
        return {key: value for key, value in zip(self.HEAD, self.DATA)}

class MPolygon(BaseModel):
    """
    Polygon
    """
    outerPolygon: gsdPoints = dataclass_field(default=gsdPoints(HEAD=["x", "y"],
                                                                DATA=[[0.0, 400.0, 400.0, 0.0], [0.0, 0.0, 600.0, 600.0]]), description="Outer polygon")

    class Config:
        title = "Polygon"

@auto_schema
def input_polygon(points: gsdPoints) -> MPolygon:
    return MPolygon(outerPolygon=points)

@auto_schema
def calc_sectprop(polygon: MPolygon) -> MSectionProperty:
    converted_coords = [[polygon.outerPolygon.DATA[0][i], polygon.outerPolygon.DATA[1][i]] for i in range(len(polygon.outerPolygon.DATA[0]))]
    converted_coords.append(converted_coords[0])
    geom = Geometry(Polygon(converted_coords))
    geom.create_mesh(mesh_sizes=100.0)

    section = Section(geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    return MSectionProperty(HEAD=["Area", "Asy", "Asz", "Ixx", "Iyy", "Izz", "Cy", "Cz", "Syp", "Sym", "Szp", "Szm", "Ipyy", "Ipzz", "Zy", "Zz", "ry", "rz"],
                            DATA=[section.get_area(), section.get_as()[0], section.get_as()[1], section.get_j(), section.get_ic()[0], section.get_ic()[1],
                                  section.get_c()[0], section.get_c()[1], section.get_z()[0], section.get_z()[1], section.get_z()[2], section.get_z()[3],
                                  section.get_ip()[0], section.get_ip()[1], section.get_s()[0], section.get_s()[1], section.get_rc()[0], section.get_rc()[1]])

@auto_schema
def report_sectprop(sectprop: MSectionProperty) -> str:
    rpt = ReportUtil("sectprop.md", "*Section Properties*")
    sect_data = sectprop.to_dict()
    rpt.add_line_fvu("Area", sect_data['Area'], enUnit.AREA)
    rpt.add_line_fvu("Asy", sect_data['Asy'], enUnit.AREA)
    rpt.add_line_fvu("Asz", sect_data['Asz'], enUnit.AREA)
    rpt.add_line_fvu("Ixx", sect_data['Ixx'], enUnit.INERTIA)
    rpt.add_line_fvu("Iyy", sect_data['Iyy'], enUnit.INERTIA)
    rpt.add_line_fvu("Izz", sect_data['Izz'], enUnit.INERTIA)
    rpt.add_line_fvu("Cy", sect_data['Cy'], enUnit.LENGTH)
    rpt.add_line_fvu("Cz", sect_data['Cz'], enUnit.LENGTH)
    rpt.add_line_fvu("Syp", sect_data['Syp'], enUnit.VOLUME)
    rpt.add_line_fvu("Sym", sect_data['Sym'], enUnit.VOLUME)
    rpt.add_line_fvu("Szp", sect_data['Szp'], enUnit.VOLUME)
    rpt.add_line_fvu("Szm", sect_data['Szm'], enUnit.VOLUME)
    rpt.add_line_fvu("Ipyy", sect_data['Ipyy'], enUnit.INERTIA)
    rpt.add_line_fvu("Ipzz", sect_data['Ipzz'], enUnit.INERTIA)
    rpt.add_line_fvu("Zy", sect_data['Zy'], enUnit.VOLUME)
    rpt.add_line_fvu("Zz", sect_data['Zz'], enUnit.VOLUME)
    rpt.add_line_fvu("ry", sect_data['ry'], enUnit.LENGTH)
    rpt.add_line_fvu("rz", sect_data['rz'], enUnit.LENGTH)
    return rpt.get_md_text()
