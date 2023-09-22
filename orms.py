from extensions import db
from datetime import datetime

class DoctorsORM(db.Model):
    doct_id=db.Column(db.Integer,primary_key=True)
    doct_name=db.Column(db.String(64),nullable=False)
    doct_phone=db.Column(db.String(11),nullable=False,unique=True)
    doct_password=db.Column(db.String(64),nullable=False)
    doct_address=db.Column(db.String(128))

    def save(self):
         db.session.add(self)
         db.session.commit()


    def query_by_phone_and_password(self, phone, password):
        print(password)
        print(phone)
        re_doctor=self.query.filter_by(doct_phone=phone, doct_password=password).first()
        return True,re_doctor if re_doctor else False

class PatientsORM(db.Model):
    pati_id=db.Column(db.Integer,primary_key=True)
    pati_name=db.Column(db.String(64),nullable=False)
    pati_gender=db.Column(db.String(11),nullable=False)
    pati_phone=db.Column(db.String(11),nullable=False,unique=True)
    pati_age=db.Column(db.String(11),nullable=False)#年龄
    pati_desc=db.Column(db.String(255), nullable=False)#治疗方案
    pati_expri=db.Column(db.String(255), nullable=False)#治疗经历
    pati_zhenduan=db.Column(db.String(255), nullable=False)

    def save(self):
         db.session.add(self)
         db.session.commit()
#在命令行用sql语句创建dpre表，存储医生id和病人id

class DpreORM(db.Model):
    dp_id = db.Column(db.Integer, primary_key=True)
    doct_id = db.Column(db.Integer, db.ForeignKey('doctors_orm.doct_id'))
    pati_id = db.Column(db.Integer, db.ForeignKey('patients_orm.pati_id'))

    def save(self):
        db.session.add(self)
        db.session.commit()


