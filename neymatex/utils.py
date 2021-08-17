import datetime
import io

import xlsxwriter
from django.http.response import FileResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa


def export_excel(columns, queryset, model_name):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True})
    worksheet = workbook.add_worksheet('Data')
    row_num = 0
    columns = list(columns.keys())
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])
    for row in queryset:
        row_num += 1
        for col_num, col_data in enumerate(row):
            if isinstance(col_data, datetime.datetime):
                col_data = col_data.strftime("%m/%d/%Y")
            worksheet.write(row_num, col_num, col_data)
    workbook.close()
    output.seek(0)
    filename = 'reporte-{}-{}.{}'.format(model_name,
                                         str(datetime.datetime.now()), 'xlsx')
    response = FileResponse(
        output,
        as_attachment=True,
        filename=filename
    )
    return response


def export_pdf(columns, queryset, model_name):
    output = io.BytesIO()
    filename = 'reporte-{}-{}.{}'.format(model_name,
                                         str(datetime.datetime.now()), 'pdf')
    context = {'columns': columns, 'qs': queryset, 'model_name': model_name}
    template = get_template('export_records_pdf.html')
    html = template.render(context)
    p = pisa.CreatePDF(html, output)
    output.seek(0)
    response = FileResponse(
        output,
        as_attachment=True,
        filename=filename
    )
    return response
