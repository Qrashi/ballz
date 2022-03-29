from datetime import datetime
from openpyxl import Workbook, worksheet

import sim.data


# Gather data and export it into an excel file
def export_excel():
    """
    Export data into an excel file
    :return:
    """
    workbook = Workbook()
    workbook.create_sheet("all data")
    workbook.create_sheet("performance")

    simdata = workbook["performance"]
    simdata.sheet_properties.tabColor = "d6af15"
    sheet_setup(simdata)
    alldata = workbook["all data"]
    alldata.sheet_properties.tabColor = "15d6d6"
    alldatacolumn = 2
    sheet_setup(workbook["all data"])

    for sceneobj in sim.scene.objects():
        workbook.create_sheet(sceneobj.name)
        sheet = workbook[sceneobj.name]
        sheet.sheet_properties.tabColor = "802f8e"
        # sheet_setup(sheet)
        cell = 1
        for plot, data in sceneobj.data.items():
            sheet.cell(row=1, column=cell).value = plot
            alldata.cell(row=1, column=alldatacolumn).value = sceneobj.name + " - " + plot
            row = 2
            for point in data:
                sheet.cell(row=row, column=cell).value = point
                alldata.cell(row=row, column=alldatacolumn).value = point
                row += 1
            cell += 1
            alldatacolumn += 1

    workbook.save(f"export{round(datetime.now().timestamp(), 0)}.xlsx")


def sheet_setup(sheet: worksheet):
    sheet.cell(row=1, column=1).value = "dalta t [s]"

    iteration = 2
    for delta_t in sim.data.delta_t:
        sheet.cell(row=iteration, column=1).value = delta_t
        iteration += 1


