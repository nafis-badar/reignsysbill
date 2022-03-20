from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
import io
from django.http import HttpResponse
from django.template.loader import get_template
# import cStringIO as StringIO
from django.template import RequestContext
#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.
 
from xhtml2pdf import pisa  
#difine render_to_pdf() function
 
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     #This part will create the pdf.
    #  pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result,)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = io.StringIO()
#     pdf = pisa.pisaDocument(io.StringIO(html.encode("UTF-8")),result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None
