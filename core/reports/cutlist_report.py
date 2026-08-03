from datetime import datetime
import os


class CutListReport:


    def __init__(self):

        self.Title = "Bosqo - Informe de fabricación"



    def generateHTML(
        self,
        cutlist,
        filename=None
    ):


        if filename is None:

            filename = os.path.join(
                os.path.expanduser("~"),
                "Bosqo_CutList_Report.html"
            )


        html = []


        html.append(
            """
            <html>
            <head>

            <meta charset="utf-8">

            <style>

            body {
                font-family: Arial;
                margin: 30px;
            }


            h1 {
                font-size: 26px;
            }


            table {

                border-collapse: collapse;
                width:100%;

            }


            th {

                background:#dddddd;

            }


            td, th {

                border:1px solid #999;
                padding:6px;
                text-align:center;

            }


            .section {

                margin-top:35px;

            }


            </style>

            </head>

            <body>
            """
        )


        #
        # Header
        #

        html.append(
            f"<h1>{self.Title}</h1>"
        )


        html.append(
            f"<p><b>Proyecto:</b> {cutlist.Project}</p>"
        )


        html.append(
            f"<p><b>Fecha:</b> {datetime.now()}</p>"
        )



        #
        # Parts
        #

        html.append(
            "<div class='section'>"
        )


        html.append(
            "<h2>Lista de piezas</h2>"
        )


        html.append(
            """
            <table>

            <tr>

            <th>Código</th>
            <th>Nombre</th>
            <th>Rol</th>
            <th>Largo</th>
            <th>Ancho</th>
            <th>Espesor</th>
            <th>Cantidad</th>
            <th>Material</th>
            <th>Acabado</th>
            <th>Veta</th>

            </tr>
            """
        )


        for item in cutlist.Items:


            html.append(

                f"""

                <tr>

                <td>{item.Code}</td>

                <td>{item.Name}</td>

                <td>{item.Role}</td>

                <td>{item.Length}</td>

                <td>{item.Width}</td>

                <td>{item.Thickness}</td>

                <td>{item.Quantity}</td>

                <td>{item.Material}</td>

                <td>{item.Finish}</td>

                <td>{item.GrainDirection}</td>

                </tr>

                """

            )


        html.append(
            "</table>"
        )


        html.append(
            "</div>"
        )



        #
        # Edges
        #

        html.append(
            "<div class='section'>"
        )


        html.append(
            "<h2>Cantos</h2>"
        )


        html.append(
            """
            <table>

            <tr>
            <th>Pieza</th>
            <th>Superior</th>
            <th>Inferior</th>
            <th>Izquierdo</th>
            <th>Derecho</th>
            </tr>

            """
        )


        for item in cutlist.Items:


            html.append(

                f"""

                <tr>

                <td>{item.Name}</td>

                <td>{item.EdgeTop}</td>

                <td>{item.EdgeBottom}</td>

                <td>{item.EdgeLeft}</td>

                <td>{item.EdgeRight}</td>

                </tr>

                """

            )


        html.append(
            "</table>"
        )


        html.append(
            "</div>"
        )



        #
        # Summary
        #

        summary = cutlist.Summary


        html.append(
            "<div class='section'>"
        )


        html.append(
            "<h2>Resumen</h2>"
        )


        html.append(

            f"""

            <p>Total piezas:
            {summary.TotalParts}</p>

            <p>Piezas diferentes:
            {summary.TotalUniqueParts}</p>

            <p>Materiales:
            {summary.TotalMaterials}</p>

            <p>Superficie total:
            {summary.TotalArea}</p>

            <p>Volumen total:
            {summary.TotalVolume}</p>

            <p>Operaciones:
            {summary.TotalOperations}</p>

            <p>Longitud de canto:
            {summary.TotalEdgeLength}</p>

            """

        )


        html.append(
            "</div>"
        )


        html.append(
            "</body></html>"
        )



        content = "\n".join(
            html
        )


        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                content
            )


        return filename



    def openHTML(
        self,
        filename
    ):

        import webbrowser

        webbrowser.open(
            filename
        )