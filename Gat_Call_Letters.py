from fastapi import  APIRouter
from .. import schemas,database,models,oauth2
from typing import List
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from fastapi import FastAPI,Depends,status,Response,HTTPException
from ..database import engine, SessionLocal,get_db
from sqlalchemy.orm import Session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
 

router=APIRouter(
    tags=['Gat_Call_Letter'])

@router.post('/gat_call_letter', status_code=status.HTTP_201_CREATED )
def create(request:schemas.Gat_call_letter,db:Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)):
    new_users=models.Gat_call_letter(
          fullname=request.fullname,
          appno=request.appno,
          email_id=request.email_id,
          mobileno=request.mobileno,
          gender=request.gender,
          gat_crtical=request.gat_crtical,
          gat_quant=request.gat_quant,
          gat_writing=request.gat_writing,
          gat_total=request.gat_total,
          gat_percentage=request.gat_percentage,
          psychometric_score=request.psychometric_score,
          gre_awa=request.gre_awa,
          gre_total=request.gre_total,
          toefl=request.toefl,
          ielts=request.ielts,
          exam_type=request.exam_type,
          rank=request.rank,
          cdate=request.cdate,
          ctime=request.ctime,
          gen_status=request.gen_status,
          email_status=request.email_status)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    return new_users

@router.get('/generate_callLetters',response_model=List[schemas.show_Gat_call_Letter])
def all(db: Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)):
      users=db.query(models.Gat_call_letter).all()
      path="./gatcallletters/"
## for multiple users
      for z in range(len(users)):
            fileName = path+users[z].appno+".pdf"
            documentTitle = 'Document title!'
            title = 'Consortium of Institutions of Higher Learning'
            subTitle = 'IIIT Campus, Gachibowli,Hyderabad - 32, Phone:: 040-24001970 Mobile: 7799834583 / 84 / 85'
            textLines = [
          'Master of Science in Information Technology'
          ]
            call=[
              'CALL LETTER'
            ]
            date=[
              'Date :' + users[z].cdate
            ]
            image ='msit.JPEG'
            a=[
              ' Dear Mr. / Ms. :' + users[z].fullname 
            ]
            b=['Sub: MSIT 2020 - Counseling and Allotment of MSIT Learning Center,'
          ]
            paragraph1=['Thank You for completing the online counseling registration process. You are required to appear for',
                      'the counseling for allotment of seat in MSIT Learning Center at IIITH/JNTUH/JNTUK/JNTUA/SVU',
                      '(direct admission) at the following online zoom link on the date and time mentioned below. Allotment ',
                      'of seats are as per the GAT/GRE ranks and subject to availability of seats in the learning centers.'
          ]
            g=['Online zoom link:' + users[z].gat_writing
          ]
            h=['Meeting ID                                 :'  + users[z].gre_awa
          ]
            i=['Meeting Password                    :'+ users[z].gat_quant
          ]
            j=['Date and Time                           :'    + users[z].cdate + users[z].ctime
          ]
            k=['MSIT Rank                                 :'+ users[z].rank   
          ]
            l=['Hall Ticket/Reference Number :'+ users[z].appno
          ]
            m=['Admission fee paid                   : ' + users[z].gat_crtical 
          ]
            n=['Payment reference ID                   : ' + users[z].gen_status  
          ]
            o=['Date of payment                        : '+ users[z].email_status
          ]
            paragraph =[
              'The balance amount of annual fee has to be paid after admissions on the reporting/induction day.',
              'The amount paid is non refundable, if admission is taken. Loan documents for bank loan purpose',
              'will be issued on the counseling day. Please join online counseling zoom link only in the',
              'specified time above (slot given to you).'
          ]
            par=['For any reason if you are unable to participate in the counseling at scheduled slot/time then it will be',
              'considered as absent, counseling process will go on and the seat will be allotted to the next rank holder.',
              'Absentees can only obtain seats in the second phase of counseling, for the remaining/available seats as ',
              'per rank order.'
          ]
            note=['Note:'
          ]
            points=['1. If you are not able to secure seat as per GAT/GRE rank the amount of Rs.30,000 paid online will be',
              '    refunded.',
                  '2. Please call help line numbers 7799834583, 7799834584, 7799834585 if you are having any difficulties',
                        '  during admissions process.',
                  '3. The amount paid is non refundable, if admission is taken.', 
                  '4. If you need training material on zoom meetings, please go through document at this link',
                                  'https://bit.ly/30qKSCr'
          ]
            leftimage = 'sign.JPEG'
            p=['Dean,'
          ]
            q=['CIHL, MSIT Division,'
          ]
            
            pdf = canvas.Canvas(fileName)
            pdf.setTitle(documentTitle)
            pdf.setFont('Helvetica-Bold', 23)
            pdf.drawCentredString(300, 770, title)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(290,740, subTitle)
            pdf.line(40, 720, 560, 720)
            text = pdf.beginText(170, 680)
            text.setFont("Helvetica-Bold", 13)
            text.setFillColor(colors.black)
            for line in textLines:
              text.textLine(line)
            pdf.drawText(text)
              #call
            text = pdf.beginText(240, 630)
            text.setFont("Helvetica-Bold", 15)
            text.setFillColor(colors.black)
            for line in call:
              text.textLine(line)
            pdf.drawText(text)
          #date
            text = pdf.beginText(500, 640)
            text.setFont("Helvetica-Bold", 11)
            text.setFillColor(colors.black)
            for line in date:
              text.textLine(line)

            pdf.drawText(text)
            text = pdf.beginText(60, 600)
            text.setFont("Helvetica-Bold", 11)
            text.setFillColor(colors.black)
            for line in a:
              text.textLine(line)
            pdf.drawText(text)

          #b
            text = pdf.beginText(60, 580)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in b:
              text.textLine(line)

            pdf.drawText(text)
          
          #paragraph1
            text = pdf.beginText(60, 560)
            text.setFont("Helvetica", 11, )
            text.setFillColor(colors.black)
            for line in paragraph1:
              text.textLine(line)

            pdf.drawText(text)
          
          #g
            text = pdf.beginText(60, 500)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in g:
              text.textLine(line)

            pdf.drawText(text)

          #h
            text = pdf.beginText(60, 480)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in h:
              text.textLine(line)

            pdf.drawText(text)

          #i
            text = pdf.beginText(60,460 )
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in i:
              text.textLine(line)

            pdf.drawText(text)

          #j
            text = pdf.beginText(60, 440)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in j:
              text.textLine(line)

            pdf.drawText(text)

          #k
            text = pdf.beginText(60, 420)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in k:
              text.textLine(line)

            pdf.drawText(text)

          #l
            text = pdf.beginText(60, 400)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in l:
              text.textLine(line)

            pdf.drawText(text)

          #m
            text = pdf.beginText(60,380 )
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in m:
              text.textLine(line)

            pdf.drawText(text)

          #n
            text = pdf.beginText(60,360 )
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in n:
              text.textLine(line)

            pdf.drawText(text)

          #o
            text = pdf.beginText(60, 340)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in o:
              text.textLine(line)

            pdf.drawText(text)
          
          #paragraph
            text = pdf.beginText(60, 320)
            text.setFont("Helvetica", 11, )
            text.setFillColor(colors.black)
            for line in paragraph:
              text.textLine(line)

            pdf.drawText(text)
          
          #par
            text = pdf.beginText(60, 260)
            text.setFont("Helvetica-Bold", 10, )
            text.setFillColor(colors.black)
            for line in par:
              text.textLine(line)

            pdf.drawText(text)
          
          #note
            text = pdf.beginText(60, 195)
            text.setFont("Helvetica-Bold", 11, )
            text.setFillColor(colors.black)
            for line in note:
              text.textLine(line)

            pdf.drawText(text)
          
          #points
            text = pdf.beginText(60, 180)
            text.setFont("Helvetica", 11, )
            text.setFillColor(colors.black)
            for line in points:
              text.textLine(line)

            pdf.drawText(text)
          
          #p
            text = pdf.beginText(60, 60)
            text.setFont("Helvetica", 11, )
            text.setFillColor(colors.black)
            for line in p:
              text.textLine(line)

            pdf.drawText(text)

          #q
            text = pdf.beginText(60, 48)
            text.setFont("Helvetica", 11, )
            text.setFillColor(colors.black)
            for line in q:
              text.textLine(line)

            pdf.drawText(text)

          #r
            

          # ###################################
          # 5) Draw a image
            pdf.drawInlineImage(image, 60, 640,  width=110, height=39)
            pdf.drawInlineImage(leftimage, 60, 70,  width=110, height=20)

            pdf.save()
################# gatcallletter for single user ############

@router.get('/gatcallletter/{email_id}}', status_code=200,response_model=List[schemas.show_Gat_call_Letter])
def show(email_id,response: Response,db: Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)):
      users=db.query(models.Gat_call_letter).filter(models.Gat_call_letter.email_id==email_id).first()
      path="./gatcallletters/"
      fileName =path+users.email_id+".pdf"
      documentTitle = 'Document title!'
      title = 'Consortium of Institutions of Higher Learning'
      subTitle = 'IIIT Campus, Gachibowli,Hyderabad - 32, Phone:: 040-24001970 Mobile: 7799834583 / 84 / 85'
      textLines = [
          'Master of Science in Information Technology'
          ]
      call=[
              'CALL LETTER'
            ]
      date=[
              'Date :' + users.cdate
            ]
      image ='msit.JPEG'
      a=[
              ' Dear Mr. / Ms. :' + users.fullname 
            ]
      b=['Sub: MSIT 2020 - Counseling and Allotment of MSIT Learning Center,'
          ]
      paragraph1=['Thank You for completing the online counseling registration process. You are required to appear for',
                      'the counseling for allotment of seat in MSIT Learning Center at IIITH/JNTUH/JNTUK/JNTUA/SVU',
                      '(direct admission) at the following online zoom link on the date and time mentioned below. Allotment ',
                      'of seats are as per the GAT/GRE ranks and subject to availability of seats in the learning centers.'
          ]
      g=['Online zoom link:' + users.gat_writing
          ]
      h=['Meeting ID                                 :'  + users.gre_awa
          ]
      i=['Meeting Password                    :'+ users.gat_quant
          ]
      j=['Date and Time                           :'    + users.cdate + users.ctime
          ]
      k=['MSIT Rank                                 :'+ users.rank   
          ]
      l=['Hall Ticket/Reference Number :'+ users.appno
          ]
      m=['Admission fee paid                   : ' + users.gat_crtical 
          ]
      n=['Payment reference ID                   : ' + users.gen_status  
          ]
      o=['Date of payment                        : '+ users.email_status
          ]
      paragraph =[
              'The balance amount of annual fee has to be paid after admissions on the reporting/induction day.',
              'The amount paid is non refundable, if admission is taken. Loan documents for bank loan purpose',
              'will be issued on the counseling day. Please join online counseling zoom link only in the',
              'specified time above (slot given to you).'
          ]
      par=['For any reason if you are unable to participate in the counseling at scheduled slot/time then it will be',
              'considered as absent, counseling process will go on and the seat will be allotted to the next rank holder.',
              'Absentees can only obtain seats in the second phase of counseling, for the remaining/available seats as ',
              'per rank order.'
          ]
      note=['Note:'
          ]
      points=['1. If you are not able to secure seat as per GAT/GRE rank the amount of Rs.30,000 paid online will be',
              '    refunded.',
                  '2. Please call help line numbers 7799834583, 7799834584, 7799834585 if you are having any difficulties',
                        '  during admissions process.',
                  '3. The amount paid is non refundable, if admission is taken.', 
                  '4. If you need training material on zoom meetings, please go through document at this link',
                                  'https://bit.ly/30qKSCr'
          ]
      leftimage = 'sign.JPEG'
      p=['Dean,'
          ]
      q=['CIHL, MSIT Division,'
          ]
      r=['CIHL, MSIT Division,'
          ]
      pdf = canvas.Canvas(fileName)
      pdf.setTitle(documentTitle)
      pdf.setFont('Helvetica-Bold', 23)
      pdf.drawCentredString(300, 770, title)
      pdf.setFillColorRGB(0, 0, 0)
      pdf.setFont("Helvetica-Bold", 11)
      pdf.drawCentredString(290,740, subTitle)
      pdf.line(40, 720, 560, 720)
      text = pdf.beginText(170, 680)
      text.setFont("Helvetica-Bold", 13)
      text.setFillColor(colors.black)
      for line in textLines:
              text.textLine(line)
      pdf.drawText(text)
              #call
      text = pdf.beginText(240, 630)
      text.setFont("Helvetica-Bold", 15)
      text.setFillColor(colors.black)
      for line in call:
              text.textLine(line)
      pdf.drawText(text)
          #date
      text = pdf.beginText(500, 640)
      text.setFont("Helvetica-Bold", 11)
      text.setFillColor(colors.black)
      for line in date:
              text.textLine(line)

      pdf.drawText(text)
      text = pdf.beginText(60, 600)
      text.setFont("Helvetica-Bold", 11)
      text.setFillColor(colors.black)
      for line in a:
              text.textLine(line)
      pdf.drawText(text)

          #b
      text = pdf.beginText(60, 580)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in b:
              text.textLine(line)

      pdf.drawText(text)
          
          #paragraph1
      text = pdf.beginText(60, 560)
      text.setFont("Helvetica", 11, )
      text.setFillColor(colors.black)
      for line in paragraph1:
              text.textLine(line)

      pdf.drawText(text)
          
          #g
      text = pdf.beginText(60, 500)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in g:
              text.textLine(line)

      pdf.drawText(text)

          #h
      text = pdf.beginText(60, 480)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in h:
              text.textLine(line)

      pdf.drawText(text)

          #i
      text = pdf.beginText(60,460 )
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in i:
              text.textLine(line)

      pdf.drawText(text)

          #j
      text = pdf.beginText(60, 440)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in j:
              text.textLine(line)

      pdf.drawText(text)

          #k
      text = pdf.beginText(60, 420)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in k:
              text.textLine(line)

      pdf.drawText(text)

          #l
      text = pdf.beginText(60, 400)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in l:
              text.textLine(line)

      pdf.drawText(text)

          #m
      text = pdf.beginText(60,380 )
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in m:
              text.textLine(line)

      pdf.drawText(text)

          #n
      text = pdf.beginText(60,360 )
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in n:
              text.textLine(line)

      pdf.drawText(text)

          #o
      text = pdf.beginText(60, 340)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in o:
              text.textLine(line)

      pdf.drawText(text)
          
          #paragraph
      text = pdf.beginText(60, 320)
      text.setFont("Helvetica", 11, )
      text.setFillColor(colors.black)
      for line in paragraph:
              text.textLine(line)

      pdf.drawText(text)
          
          #par
      text = pdf.beginText(60, 260)
      text.setFont("Helvetica-Bold", 10, )
      text.setFillColor(colors.black)
      for line in par:
              text.textLine(line)

      pdf.drawText(text)
          
          #note
      text = pdf.beginText(60, 195)
      text.setFont("Helvetica-Bold", 11, )
      text.setFillColor(colors.black)
      for line in note:
              text.textLine(line)

      pdf.drawText(text)
          
          #points
      text = pdf.beginText(60, 180)
      text.setFont("Helvetica", 11, )
      text.setFillColor(colors.black)
      for line in points:
              text.textLine(line)

      pdf.drawText(text)
          
          #p
      text = pdf.beginText(60, 60)
      text.setFont("Helvetica", 11, )
      text.setFillColor(colors.black)
      for line in p:
              text.textLine(line)

      pdf.drawText(text)

          #q
      text = pdf.beginText(60, 48)
      text.setFont("Helvetica", 11, )
      text.setFillColor(colors.black)
      for line in q:
              text.textLine(line)

      pdf.drawText(text)

          #r
      text = pdf.beginText(60, 36)
      text.setFont("Helvetica", 11, )
      text.setFillColor(colors.black)
      for line in r:
              text.textLine(line)

      pdf.drawText(text)

          # ###################################
          # 5) Draw a image
      pdf.drawInlineImage(image, 60, 640,  width=110, height=39)
      pdf.drawInlineImage(leftimage, 60, 70,  width=110, height=20)

      pdf.save()

            

          




####################################### 

