from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.platypus import Image, Paragraph, Spacer, Table
from reportlab.rl_config import defaultPageSize

from mainsite.helpers import generate_pdf_report_download_response, reportlab_table_style, reportlab_get_image
from purchases.models import ExpenseMonth, ExpenseStatement


def generate_fiscal_report(filename, pk):
    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]
    styles = getSampleStyleSheet()

    em = ExpenseMonth.objects.get(pk=pk)
    st = ExpenseStatement.objects.get(
        card=em.card, month=em.month, year=em.year
    )
    card_ems = ExpenseMonth.objects.filter(
        card=em.card, month=em.month, year=em.year
    )
    # Report title
    title = 'Statement for card %s in %s/%s' % (
        em.card.last4, em.month, em.year
    )
    # Card statement
    statementData = [
        ['Date', 'Item', 'Amount']
    ]
    for item in st.items.all():
        statementData.append([
            item.date.strftime('%m/%d/%Y'), item.description, item.amount
        ])
    statementTable = Table(statementData, style=reportlab_table_style)
    # ReportLab Platypus flowables
    flowables = [
        Paragraph(f'Statement Total: ${st.total}', styles['Heading2']),
        statementTable
    ]
    # Card Expense Months
    pdf_receipts = [] # PDF files to merge at the end
    for em in card_ems:
        for expense in em.expenses.all():
            # Add receipt file
            if expense.receipt:
                if expense.receipt.file.name.lower().endswith('.pdf'):
                    pdf_receipts.append(expense.receipt.file)
                else:
                    flowables.append(reportlab_get_image(expense.receipt.file.name, width=PAGE_WIDTH-2*inch))
                    # flowables.append(Image(expense.receipt.file, width=100, height=100))

    return generate_pdf_report_download_response(filename, title, flowables, pdf_receipts)