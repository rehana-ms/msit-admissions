from fastapi  import  APIRouter
from .. import schemas,database,models,oauth2
from typing import List
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from ..database import engine, SessionLocal,get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,Response,HTTPException
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER


router=APIRouter(
      tags=['GatHalltickets']
      )

@router.post('/gat_hallticket',status_code=status.HTTP_201_CREATED)
def create(request:schemas.GatHallticket,db : Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)):
      gat_user=models.GatHallticket(
            id=request.id,
            email_id=request.email_id,
            username=request.full_name,
            phoneno=request.mobile_no,
            image_url=request.image_url,
            gatAppNo=request.gatAppNo,
            center=request.center,
            examType=request.examType,
            paymentType=request.paymentType,
            paymentsStatus=request.paymentStatus,
            testDate=request.testDate,
            testTime=request.testTime,
            htStatus=request.htStatus,
            emailStatus=request.emailStatus,
            htTime=request.htTime,
            emailTime=request.emailTime)
      db.add(gat_user)
      db.commit()
      db.refresh(gat_user)
      return gat_user

@router.get('/generate_GatHallticket',response_model=List[schemas.ShowGatuser])
def all(db: Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)):
      users=db.query(models.GatHallticket).all()
      path="./gathalltickets/"
      for i in range(len(users)):
          filename =path+users[i].email_id+".pdf"
          can = canvas.Canvas(filename)
          
          can.setFont("Helvetica-Bold", 20)
          can.drawString(75, 780, "Consortium of Institutions of Higher Learning")

          can.setFont("Helvetica-Bold", 11)
          can.drawString(60, 760, 'IIIT Campus, Gachibowli,Hyderabad - 32, Phone:: 040-24001970 Mobile: 7799834583 / 84 / 85')

          can.line(40, 740, 560, 740)

          can.setFont("Helvetica-Bold", 14)
          can.drawString(130, 720, 'Master of Science in Information Technology')

          can.setFont("Helvetica-Bold", 14)
          can.drawString(210, 690, 'Entrance Test 2021' )

          can.setFont("Helvetica-Bold", 14)
          can.drawString(225, 670, 'HALL TICKET')

          can.drawImage('msit.JPEG',60, 640,  width=110, height=39 )

          can.setFont("Helvetica-Bold", 11)
          can.drawString(60, 590,  'Hall Ticket No :'+ users[i].gatAppNo)

          can.setFont("Helvetica-Bold", 11)
          can.drawString(60, 560, 'Name of the Candidate : '+ users[i].username)

          can.setFont("Helvetica-Bold", 11)
          can.drawString(60, 530, 'Payment Type : '+ users[i].paymentType)
          profile_img="./profile_images/"+users[i].email_id+".JPG"
          can.drawImage(profile_img, 450, 500,  width=110, height=110 )
#############

          width, height = A4
          styles = getSampleStyleSheet()
          styleN = styles["BodyText"]
          styleN.alignment = TA_LEFT
          styleBH = styles["Normal"]
          styleBH.alignment = TA_CENTER

          def coord(x, y, unit=1):
              x, y = x * unit, height -  y * unit
              return x, y
          


          # Headers
          hVenue = Paragraph('''<b>Venue</b>''', styleBH)
          hTime = Paragraph('''<b>Time & Date of the Test</b>''', styleBH)


          # Texts
          Venue = Paragraph('Eduquity Career Technologies PVT LTD,403, 4th Floor, Myhome Sarovar Plaza,Behind British Library, adjacent to medi city, Secretariat road, Hyderabad-63 Ph:040-23243010',styleN)
          Time  = Paragraph('2021-05-12  10:00 A.M.', styleN)

          data= [[hVenue, hTime],
                [Venue,Time]]

          table = Table(data, colWidths=[7* cm, 3* cm, 6 * cm,
                                        5* cm, 5 * cm])

          table.setStyle(TableStyle([
                                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                
                                ]))


          table.wrapOn(can, width, height)
          table.drawOn(can, *coord(6, 16, cm))

          can.setFont("Helvetica-Bold", 14)
          can.drawString(60, 360, 'Instructions for Candidates:')

          can.setFont("Helvetica", 11)
          can.drawString(60, 340, '1. If you did not pay through online, please carry your DD along with this hall ticket form, without fail.')
          can.setFont("Helvetica", 11)                
          can.drawString(60, 320, '2. Any error/change in your name/address must be communicated immediately through')
          can.setFont("Helvetica", 11)  
          can.drawString(60, 307,"    email to : enquiries2015@msitprogram.net.") 
          can.setFont("Helvetica", 11)  
          can.drawString(60, 290,'3. The candidate is being conditionally allowed to appear in the entrance examination,without verifying')
          can.setFont("Helvetica", 11)  
          can.drawString(60, 277,'    whether he/she satisfies the eligibility criterion. This will be examined,at the time of final admission,' )
          can.setFont("Helvetica", 11)  
          can.drawString(60, 265,'    if granted.' )
        

          can.drawImage('sign.JPG', 450, 235,  width=110, height=20)

          can.setFont("Helvetica-Bold", 11)  
          can.drawString(450, 220,'  (Dean,CIHL)' )

          can.setFont("Helvetica-Bold", 10)  
          can.drawString(60, 200,'       Signature of the Candidate' )


          
          can.showPage()
          can.save()
          
################# gatcallletter for single user ############
@router.get('/gathallticket/{email_id}}', status_code=200,response_model=List[schemas.ShowGatuser])
def show(email_id,response: Response,db: Session=Depends(get_db),get_current_user:schemas.Admin=Depends(oauth2.get_current_user)):
      users=db.query(models.GatHallticket).filter(models.GatHallticket.email_id==email_id).first()
      path="./gathalltickets/"
      filename = path+users.email_id+".pdf"
      can = canvas.Canvas(filename)
          
      can.setFont("Helvetica-Bold", 20)
      can.drawString(75, 780, "Consortium of Institutions of Higher Learning")

      can.setFont("Helvetica-Bold", 11)
      can.drawString(60, 760, 'IIIT Campus, Gachibowli,Hyderabad - 32, Phone:: 040-24001970 Mobile: 7799834583 / 84 / 85')

      can.line(40, 740, 560, 740)

      can.setFont("Helvetica-Bold", 14)
      can.drawString(130, 720, 'Master of Science in Information Technology')

      can.setFont("Helvetica-Bold", 14)
      can.drawString(210, 690, 'Entrance Test 2021' )

      can.setFont("Helvetica-Bold", 14)
      can.drawString(225, 670, 'HALL TICKET')

      can.drawImage('msit.JPEG',60, 640,  width=110, height=39 )

      can.setFont("Helvetica-Bold", 11)
      can.drawString(60, 590,  'Hall Ticket No :'+ users.gatAppNo)

      can.setFont("Helvetica-Bold", 11)
      can.drawString(60, 560, 'Name of the Candidate : '+ users.username)

      can.setFont("Helvetica-Bold", 11)
      can.drawString(60, 530, 'Payment Type : '+ users.paymentType)

      profile_img="./profile_images/"+users.email_id+".JPG"

      can.drawImage(profile_img, 450, 500,  width=110, height=110 )


      width, height = A4
      styles = getSampleStyleSheet()
      styleN = styles["BodyText"]
      styleN.alignment = TA_LEFT
      styleBH = styles["Normal"]
      styleBH.alignment = TA_CENTER

      def coord(x, y, unit=1):
              x, y = x * unit, height -  y * unit
              return x, y
          


          # Headers
      hVenue = Paragraph('''<b>Venue</b>''', styleBH)
      hTime = Paragraph('''<b>Time & Date of the Test</b>''', styleBH)


          # Texts
      Venue = Paragraph('Eduquity Career Technologies PVT LTD,403, 4th Floor, Myhome Sarovar Plaza,Behind British Library, adjacent to medi city, Secretariat road, Hyderabad-63 Ph:040-23243010',styleN)
      Time  = Paragraph('2021-05-12  10:00 A.M.', styleN)

      data= [[hVenue, hTime],
                [Venue,Time]]

      table = Table(data, colWidths=[7* cm, 3* cm, 6 * cm,
                                        5* cm, 5 * cm])

      table.setStyle(TableStyle([
                                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                
                                ]))


      table.wrapOn(can, width, height)
      table.drawOn(can, *coord(6, 16, cm))

      can.setFont("Helvetica-Bold", 14)
      can.drawString(60, 360, 'Instructions for Candidates:')

      can.setFont("Helvetica", 11)
      can.drawString(60, 340, '1. If you did not pay through online, please carry your DD along with this hall ticket form, without fail.')
      can.setFont("Helvetica", 11)                
      can.drawString(60, 320, '2. Any error/change in your name/address must be communicated immediately through')
      can.setFont("Helvetica", 11)  
      can.drawString(60, 307,"    email to : enquiries2015@msitprogram.net.") 
      can.setFont("Helvetica", 11)  
      can.drawString(60, 290,'3. The candidate is being conditionally allowed to appear in the entrance examination,without verifying')
      can.setFont("Helvetica", 11)  
      can.drawString(60, 277,'    whether he/she satisfies the eligibility criterion. This will be examined,at the time of final admission,' )
      can.setFont("Helvetica", 11)  
      can.drawString(60, 265,'    if granted.' )

      can.drawImage('sign.JPEG', 450, 235,  width=110, height=20)

      can.setFont("Helvetica-Bold", 11)  
      can.drawString(450, 220,'  (Dean,CIHL)' )

      can.setFont("Helvetica-Bold", 10)  
      can.drawString(60, 200,'       Signature of the Candidate' )


          
      can.showPage()
      can.save()
###########################

   
     
     
    
