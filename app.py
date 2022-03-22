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
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %i>' %self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        #lấy tên khách hàng và nội dung
        customer=request.form.get('khachhang')
        task_content=request.form.get('content1')
        new_task=Todo(khachhang=customer, content=task_content)
        #thêm sản phẩm vào nếu được 
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
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Có vấn đề khi thực hiện update'
    else:
        return render_template('update.html', task=task)



if __name__=='__main__':
    app.run(debug=True)