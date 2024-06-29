"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import textwrap as text
import typing as h

import PyQt6.QtCore as core
import PyQt6.QtGui as qgui
import PyQt6.QtWidgets as wdgt
from pyvispr.config.appearance.color import GRID_PEN
from pyvispr.config.appearance.geometry import GRID_RESOLUTION_H, GRID_RESOLUTION_V
from pyvispr.flow.functional.node import node_t as functional_t
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.runtime.backend import SCREEN_BACKEND


@d.dataclass(slots=True, repr=False, eq=False)
class graph_t(wdgt.QGraphicsScene):
    grid_is_visible: bool = True

    @property
    def nodes(self) -> tuple[node_t, ...]:
        """"""
        return tuple(_elm for _elm in self.items() if isinstance(_elm, node_t))

    @property
    def links(self) -> tuple[link_t, ...]:
        """"""
        return tuple(_elm for _elm in self.items() if isinstance(_elm, link_t))

    @property
    def bounding_box(self) -> tuple[float, float, float, float]:
        """
        "Spelled" clockwise from north.
        """
        if self.nodes.__len__() == 0:
            return 4 * (0.0,)

        nodes = self.nodes

        rectangle = nodes[0].sceneBoundingRect()
        north = rectangle.y()
        west = rectangle.x()
        south = north + rectangle.height()
        east = west + rectangle.width()
        for node in nodes[1:]:
            rectangle = node.sceneBoundingRect()
            position_x, position_y = rectangle.x(), rectangle.y()
            north = min(north, position_y)
            west = min(west, position_x)
            south = max(south, position_y + rectangle.height())
            east = max(east, position_x + rectangle.width())

        return north, east, south, west

    def __post_init__(self) -> None:
        """"""
        wdgt.QGraphicsScene.__init__(self)
        SCREEN_BACKEND.AddMessageCanal(self, "changed", self.UpdateLinkPaths)

    def AddNodeForFunctional(
        self,
        functional: functional_t,
        InvalidateOutputs: h.Callable[[None], None],
        /,
        *,
        and_return_it: bool = False,
    ) -> node_t | None:
        """"""
        node = node_t.NewForFunctional(functional, InvalidateOutputs)

        # Otherwise the newly created visual node replaces the selection.
        self.clearSelection()
        self.addItem(node)
        if node.ii_dialog is not None:
            self.addItem(node.ii_dialog)

        if and_return_it:
            return node

    def RemoveNode(self, node: node_t, /) -> None:
        """"""
        if node.ii_dialog is not None:
            node.ii_dialog.close()

        # Do not iterate directly on the list since it can be modified in the process.
        for link in tuple(self.links):
            if (link.source is node) or (link.target is node):
                self.RemoveLink(link)

        self.removeItem(node)
        if node.ii_dialog is not None:
            self.removeItem(node.ii_dialog)

    def AddLink(
        self, source: node_t, target: node_t, /, *, should_return_it: bool = False
    ) -> link_t | None:
        """"""
        for link in self.links:
            if (link.source is source) and (link.target is target):
                return

        link = link_t.New(
            source,
            source.output_socket_coordinates,
            target,
            target.intake_socket_coordinates,
        )
        self.addItem(link)
        self.addItem(link.arrow)

        if should_return_it:
            return link

    def RemoveLink(
        self,
        link: link_t,
        /,
    ) -> None:
        """"""
        self.removeItem(link)
        self.removeItem(link.arrow)

    def MergeWith(self, other: h.Self, /) -> None:
        """"""
        for item in other.nodes + other.links:
            self.addItem(item)
            if isinstance(item, node_t):
                item.setSelected(True)
                if item.ii_dialog is not None:
                    self.addItem(item.ii_dialog)
            else:
                self.addItem(item.arrow)

        del other

    def UpdateLinkPaths(
        self, _: h.Sequence[core.QRectF] | None, /, *, even_if_still: bool = False
    ) -> None:
        """"""
        for node in self.items():
            if isinstance(node, node_t) and (
                even_if_still or node.position_has_changed
            ):
                for link in self.links:
                    if (node is link.source) or (node is link.target):
                        link.SetPath(
                            link.source.output_socket_coordinates,
                            link.target.intake_socket_coordinates,
                        )
                node.position_has_changed = False

    def ToggleGridVisibility(self) -> None:
        """"""
        self.grid_is_visible = not self.grid_is_visible

        view = self.views()[0]
        viewport = view.viewport()
        corner = view.mapToScene(core.QPoint(0, 0))
        size = view.mapToScene(core.QPoint(viewport.width(), viewport.height()))
        self.update(core.QRectF(corner, size))

    def AlignOnGrid(self) -> None:
        """"""
        for node in self.nodes:
            node.AlignOnGrid()

    def Clear(self) -> None:
        """"""
        # Do not iterate directly on the list since it is modified in the process.
        while self.nodes.__len__() > 0:
            self.RemoveNode(self.nodes[0])

    def drawBackground(self, painter: qgui.QPainter, region: core.QRectF, /) -> None:
        """"""
        if not self.grid_is_visible:
            wdgt.QGraphicsScene.drawBackground(self, painter, region)
            return

        painter.setWorldMatrixEnabled(True)
        painter.setPen(GRID_PEN)

        north, east, south, west = (
            region.top(),
            region.right(),
            region.bottom(),
            region.left(),
        )

        vertical_s = []
        current_x = int(west) - (int(west) % GRID_RESOLUTION_H)
        while current_x < east:
            vertical_s.append(core.QLineF(current_x, north, current_x, south))
            current_x += GRID_RESOLUTION_H

        horizontal_s = []
        current_y = int(north) - (int(north) % GRID_RESOLUTION_V)
        while current_y < south:
            horizontal_s.append(core.QLineF(west, current_y, east, current_y))
            current_y += GRID_RESOLUTION_V

        painter.drawLines(vertical_s)
        painter.drawLines(horizontal_s)
        wdgt.QGraphicsScene.drawBackground(self, painter, region)

    def __str__(self) -> str:
        """"""
        output = [
            "VISUAL GRAPH",
            f"Visual nodes: {self.nodes.__len__()}",
            f"Visual links: {self.links.__len__()}",
            f"Bounding box (NESW): {str(self.bounding_box)[1:-1]}",
            "NODE(S):",
        ]

        for node in self.nodes:
            output.append(text.indent(str(node), "    "))

        output.append("LINK(S):")
        for link in self.links:
            output.append(text.indent(str(link), "    "))

        # output.extend(("", str(self.functional)))

        return "\n".join(output)


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
