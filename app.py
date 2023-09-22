import io
import random
import sqlite3
import faker
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, render_template_string, \
    send_file
from pyecharts.globals import ThemeType
from werkzeug.utils import secure_filename
from faker import Faker
from orms import DoctorsORM,PatientsORM,DpreORM
import orms
import config
from extensions import register_extension, db
import pandas as pd
import matplotlib.pyplot as plt
import base64
from pyecharts.charts import Bar, Scatter
from pyecharts import options as opts
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key='123456'

app.config.from_object(config)
register_extension(app)

@app.route('/')
def hello():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

#建表。在终端用flask create命令
@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    faker =Faker(locale="zh-CN")
    for i in range(10):
        doctor=orms.DoctorsORM()
        info = faker.simple_profile()
        doctor.doct_id=i+1000
        doctor.doct_name=info['name']
        doctor.doct_phone=faker.phone_number()
        doctor.doct_password=faker.password()
        doctor.doct_address=info['address']
        doctor.save()

    for j in range(20):
        patient = orms.PatientsORM()
        info = faker.simple_profile()
        patient.pati_id=j+100
        patient.pati_name=info['name']
        patient.pati_gender=info['sex']
        patient.pati_phone=faker.phone_number()
        patient.pati_age=faker.random_int(min=0,max=100)
        patient.pati_desc="请填写"
        patient.pati_expri=random.choice(['初始','经治'])
        patient.pati_zhenduan="诊断记录"
        patient.save()

@app.post('/api/login')
def login():
    data=request.get_json()
    print(data)
    #查询
    doctor=DoctorsORM()
    rs,rs_doctor=doctor.query_by_phone_and_password(data['mobile'],data['password'])
    if rs:
        session['doct_name']=rs_doctor.doct_name
        session['doct_address']=rs_doctor.doct_address
        session['doct_phone']=rs_doctor.doct_phone

        return{
            'message': '登录成功！',
            'code' : 0
        }
    else:
        return {
            'message': '登录失败！',
            'code': -1
        }

@app.route('/doctor')
def doctor():
    doctor_phone = session.get('doct_phone')
    doctor = DoctorsORM.query.filter_by(doct_phone=doctor_phone).first()  # doctor是该电话对应的一整行医生信息
    if doctor:
        doctor_id = doctor.doct_id  # 获取医生id

        # 根据医生ID查询医生的所有信息
        doctor_info = DoctorsORM.query.filter_by(doct_id=doctor_id).first()
        if doctor_info:
            # 构建医生信息表格
            doctor_table = f'''
                        <table>
                            <tr>
                                <th>医生ID</th>
                                <th>医生姓名</th>
                                <th>医生电话</th>
                                <th>医生地址</th>
                                <!-- 其他医生信息字段 -->
                            </tr>
                            <tr>
                                <td>{doctor_info.doct_id}</td>
                                <td>{doctor_info.doct_name}</td>
                                <td>{doctor_info.doct_phone}</td>
                                <td>{doctor_info.doct_address}</td>
                                <!-- 其他医生信息字段 -->
                            </tr>
                        </table>
                    '''
            return doctor_table
        else:
            return '医生信息不存在'
        # if doctor_info:
        #     # 返回医生的所有信息
        #     return {
        #         'code': 0,
        #         'msg': '医生信息查询成功',
        #         'data': {
        #             'doct_id': doctor_info.doct_id,
        #             'doct_name': doctor_info.doct_name,
        #             'doct_phone': doctor_info.doct_phone,
        #             'doct_address':doctor_info.doct_address
        #             # 其他医生信息字段
        #         }
        #     }
        # else:
        #     return {
        #         'code': 1,
        #         'msg': '医生信息不存在'
        #     }


@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/page1')
def page1_view():
    df=pd.read_csv(r'D:\python\test1.csv')
    table_data=df.to_dict(orient='records')#列表
    print(type(table_data))
    return render_template('page1_view.html',table_data=table_data)
#另一种方法
# @app.route('/page2')
# def create_plot():
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#     df = pd.read_csv(r'D:\python\test1.csv')
#     data = df.sort_values("rate", ascending=False)[:20]
#     result = data.set_index("name")
#     # plt.figure(figsize=(8,6))
#     plt.bar(result.index, result["rate"], color='#87CEEB', width=0.8)
#     plt.xlabel("书名")
#     plt.ylabel("评分")
#     plt.ylim(9, 10)
#     plt.title("评分排名前20的书籍")
#     plt.xticks(rotation=70)
#     # 保存图表为临时文件
#     # temp_file = 'static/temp.png'
#     # plt.savefig(temp_file)  # 可根据需要设置保存格式和其他参数
#     # plt.close()  # 关闭图表，释放资源
#     # return render_template('page2_view.html',image=temp_file)
#转化成图片
# def plot_to_img():
#     create_plot()
#     img=io.BytesIO()
#     plt.savefig(img,format='png')
#     img.seek(0)
#     img_bs4=base64.b64encode(img.getvalue()).decode()
#     return img_bs4
# @app.route('/page2')
# def plot():
#     img_b64=plot_to_img()
#     html = f'<img src="data:image/png;base64,{img_b64}" class="blog-image">'
#     return render_template_string(html)

#matplotlib画图
# def generate_matplotlib_png():
#     fig=plt.figure(figsize=(8,6))
#     plt.rcParams['font.sans-serif'] = ['SimHei']#允许显示中文
#     df = pd.read_csv(r'D:\python\test1.csv')
#     data = df.sort_values("rate", ascending=False)[:20]
#     result = data.set_index("name")
#     # plt.figure(figsize=(8,6))
#     plt.bar(result.index, result["rate"], color='#87CEEB', width=0.8)
#     plt.xlabel("书名")
#     plt.ylabel("评分")
#     plt.ylim(9, 10)
#     plt.title("评分排名前20的书籍")
#     plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)  # 调整图形的边距
#     plt.xticks(rotation=45, fontsize=8)
#     plt.tight_layout()  # 自动调整图形布局
#
#     png_name="my_matplotlib.png"
#     plt.savefig(f'./static/{png_name}')
#     plt.clf()#清除之前的图像，以便绘制新的图像
#     plt.close(fig)
#     return png_name
#
# @app.route('/page2')
# def plot():
#     matplotlib_png = generate_matplotlib_png()
#     return render_template('page2_view.html',matplotlib_png=matplotlib_png)

# def get_scatter_png():
#     fig=plt.figure()
#     df = pd.read_csv(r'D:\python\test1.csv')
#     x_data = range(0,250)
#     y_data = df['rate']
#     plt.xlabel('书本号')
#     plt.ylabel('评分')
#     plt.title('250本书的评分分布情况')
#     plt.scatter(x_data, y_data, c='#006400', marker='.')
#     plt.tight_layout()
#
#     png = "M_sactter.png"
#     plt.savefig(f'./static/{png}')
#     plt.clf()  # 清除之前的图像，以便绘制新的图像
#     plt.close(fig)
#     return png
#
# @app.route('/page3')
# def page3_view():
#     scatter_png=get_scatter_png()
#     return render_template('page3_view.html',scatter_png=scatter_png)

#获取医生对应的患者信息


#pycharts画图
def pycharts_view():
    df = pd.read_csv(r'D:\python\test1.csv')
    data = df.sort_values("rate", ascending=False)[:20]["rate"].tolist()
    name=df.sort_values("rate", ascending=False)[:20]["name"].tolist()
    bar = (#创建实例
        Bar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS,width="1200",height="800"))
        .add_xaxis(name)
        .add_yaxis("评分", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="评分排名前20的书籍"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=70)),
                         yaxis_opts=opts.AxisOpts(min_=9, max_=10))

    )
    return bar

@app.route("/page2")
def page2_view():
    pyecharts_picture=pycharts_view()
    return render_template("page2_view.html",pyecharts_option=pyecharts_picture.dump_options())

def scatter():
    df = pd.read_csv(r'D:\python\test1.csv')
    y_data=df["rate"].tolist()
    x_data=df['name'].tolist()
    scatter=(
        Scatter()
        .add_xaxis(x_data)
        .add_yaxis("评分", y_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="评分分布情况"),
                         yaxis_opts=opts.AxisOpts(min_=8.5, max_=10))
    )
    return scatter

@app.route("/page3")
def page3_view():
    scatter_picture = scatter()
    return render_template('page3_view.html', scatter_picture=scatter_picture.dump_options())



@app.route('/api/patient_table')
def doctor_view():
    # 从会话中获取医生的电话
    doctor_phone = session.get('doct_phone')
    doctor = DoctorsORM.query.filter_by(doct_phone=doctor_phone).first()#doctor是该电话对应的一整行医生信息
    if doctor:
        doctor_id =doctor.doct_id#获取医生id
        # 根据医生id从dpre表中搜索出对应的患者id列表
        patient_ids = DpreORM.query.with_entities(DpreORM.pati_id).filter_by(doct_id=doctor_id).all()
        patient_ids = [patient_id[0] for patient_id in patient_ids]

        # 根据患者ID列表从患者表中搜索出对应的患者信息
        patients = PatientsORM.query.filter(PatientsORM.pati_id.in_(patient_ids)).all()#列表
        for patient in patients:
            patient_id = patient.pati_id
            print(type(patient))
            print(type(patient_id))
        return {
            'code': 0,
            'msg': '信息查询成功',
            'count': len(patients),
            'data': [
                {
                    'pati_id': patient.pati_id,
                    'pati_name': patient.pati_name,
                    'pati_gender': patient.pati_gender,
                    'pati_phone': patient.pati_phone,
                    'pati_age': patient.pati_age,
                    'pati_desc': patient.pati_desc,
                    'pati_expri': patient.pati_expri,
                    'pati_zhenduan': patient.pati_zhenduan,
                } for patient in patients
            ]
        }
    else:
        return {
            'code': 1,
            'msg': '医生不存在'
        }
    # 查询患者信息
    paginate = PatientsORM.query.filter(PatientsORM.pati_id.in_(patient_ids)).paginate(page=page, per_page=per_page, error_out=False)


#修改诊断经历
@app.put('/api/patient/<int:sid>/desc')
def api_patient_desc(sid):
    patient: PatientsORM = db.get_or_404(PatientsORM, sid)
    data = request.get_json()
    try:
        patient.pati_desc = data['pati_desc']
        patient.save()
    except Exception as e:
        return {
            'code': -1,
            'msg': '修改治疗方案失败'
        }
    return {
        'code': 0,
        'msg': '修改治疗方案成功'
    }


if __name__ == '__main__':
    app.run(debug=True)