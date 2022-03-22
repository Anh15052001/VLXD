
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#tạo đối tượng thể hiện lớp Flask
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'

db=SQLAlchemy()
db.init_app(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    khachhang=db.Column(db.String(300), nullable=False)
    content=db.Column(db.String(2000), nullable=False)
    donvi=db.Column(db.String(200), nullable=True)
    dongia=db.Column(db.Integer, nullable=False)
    soluong=db.Column(db.Integer, nullable=False)
    thanhtien=db.Column(db.Integer, nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %i>' %self.id
with app.app_context():
    db.create_all()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        #lấy tên khách hàng và nội dung
        customer=request.form.get('khachhang')
        task_content=request.form.get('content1')
        dv=request.form.get('donvi')
        dg=request.form.get('dongia')
        sl=request.form.get('soluong')


        new_task=Todo(khachhang=customer, content=task_content, donvi=dv, dongia=dg, soluong=sl, thanhtien=int(dg)*int(sl))
        #thêm sản phẩm vào nếu được g
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Có vấn đề khi thêm khách hàng'
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

#hàm delete
@app.route('/delete/<int:id>')
def delete(id):
    #lấy id của mặt hàng cần xóa
    task_to_delete=Todo.query.get_or_404(id)
    #thực hiện xóa
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Có vấn đề khi thực hiện xóa'

#hàm update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        #lấy tên khách hàng và nội dung
        task.khachhang=request.form.get('khachhang')
        task.content=request.form.get('content1')
        #lấy đơn vị tính
        task.donvi=request.form.get('donvi')
        task.dongia=request.form.get('dongia')
        task.soluong=request.form.get('soluong')
        task.thanhtien=int(task.dongia)*int(task.soluong)
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Có vấn đề khi thực hiện update'
    else:
        return render_template('update.html', task=task)



if __name__=='__main__':
    app.run(debug=True)