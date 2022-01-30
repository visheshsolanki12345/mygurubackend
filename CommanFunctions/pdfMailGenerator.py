from django.core.mail.message import EmailMultiAlternatives
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import uuid

def pdfGenMail(context, to_email):
    template = get_template('CommanFunctions/mytemplate.html')
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = result.getvalue()
    filename = 'Result'
    filenamePDf = uuid.uuid4()
    try:
        with open(str(settings.BASE_DIR) + f'\\media\\ResultPdf\\{filenamePDf}.pdf', 'wb+') as output:
            pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), output)
            # print('.................', f'/ResultPdf/{filenamePDf}.pdf')
    except:
        pass
    try:
        mail_subject = 'Recent Result'
        message  = "this is test result"
        # to_email = user.email
        email = EmailMultiAlternatives(
                            mail_subject,
                            "hello",
                            settings.EMAIL_HOST_USER,
                            [to_email]
                        )
        email.attach_alternative(message, "text/html")
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)
    except:
        pass