from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.rl_config import defaultPageSize
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

from purchases.models import ExpenseMonth


def generate_fiscal_report(buffer, pk):
    em = ExpenseMonth.objects.get(pk=pk)
    title = 'Statement for card %s in %s/%s' % (em.card.last4, em.month, em.year)
    
    # Create the PDF object, using the buffer as its "file."
    cv = canvas.Canvas(buffer)
    # Draw stuff
    # cv.drawString(100, 100, 'Statement for *6950 (Jackalynn Low) in October 2024')

    cv.saveState()
    cv.setFont('Times-Bold',16)
    cv.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, title)
    cv.setFont('Times-Roman',9)
    cv.drawString(inch, 0.75 * inch, "First Page / %s" % 'xxx')
    cv.restoreState()

    # Close the PDF object cleanly.
    cv.showPage()
    cv.save()
    return cv