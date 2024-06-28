from super_scad.boolean.Union import Union
from super_scad.Context import Context
from super_scad.d2.Polygon import Polygon
from super_scad.d2.Text import Text
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Offset import Offset
from super_scad.transformation.Paint import Paint
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type.Color import Color
from super_scad.type.Point2 import Point2


class Logo(ScadObject):
    """
    Generates the logo of SuperSCAD.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        outline = [Point2(0.0, 0.0),
                   Point2(258.0, 257.0),
                   Point2(182.0, 401.0),
                   Point2(-182.0, 401.0),
                   Point2(-258.0, 257.0)]

        pentagon1 = Paint(color=Color(color='black'), child=Polygon(points=outline))
        pentagon2 = Paint(color=Color(color='#ff3334'), child=Offset(delta=-5.0, child=pentagon1))
        pentagon3 = Paint(color=Color(color='black'), child=Offset(delta=-28.0, child=pentagon2))
        pentagon4 = Paint(color=Color(color='#f9d72c'), child=Offset(delta=-5.0, child=pentagon3))

        text1 = Translate2D(y=278.0,
                            child=Paint(color=Color(color='#ff3334'),
                                        child=Text(text='SCAD',
                                                   size=86,
                                                   spacing=1.05,
                                                   halign='center',
                                                   valign='center')))

        text2 = Paint(color=Color(color='black'), child=Offset(delta=2.0, child=text1))

        return Union(children=[pentagon1, pentagon2, pentagon3, pentagon4, text2, text1])

# ----------------------------------------------------------------------------------------------------------------------
