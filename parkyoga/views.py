from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Suburb, Course, Order
from datetime import datetime, timedelta
from .forms import CheckoutForm
from . import db
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

# Home page add the seach function
@main_bp.route('/')
def index():
    # define the function of search function to be called  in the index.html
    query = request.args.get('q')
    if query:
        courses = db.session.scalars(db.select(Course).where(or_(Course.description.ilike(f'%{query}%'),Course.name.ilike(f'%{query}%')))).all()
        return render_template('index.html', query=query, courses=courses)
    else:
        suburbs = db.session.scalars(db.select(Suburb)).all()
        return render_template('index.html', suburbs=suburbs)
    
# View all the yoga courses of a suburb
@main_bp.route('/courses/<int:suburb_id>')
def yogacourse(suburb_id):
    courses = db.session.scalars(db.select(Course).where(Course.suburb_id==suburb_id)).all()
    suburb_name = db.session.scalar(db.select(Suburb.name).where(Suburb.id == suburb_id))
    
    # Add new dates to each course
    for course in courses:
        course.new_dates = [
            course.date,
            course.date + timedelta(days=3),
            course.date + timedelta(days=7),
            course.date + timedelta(days=10)
        ]    
    return render_template('yogacourse.html', courses=courses,suburb_name=suburb_name)

# Referred to as "Basket" to the user
@main_bp.route('/order', methods=['POST', 'GET'])
def order():
    courses_id = request.values.get('courses_id')
    # able to add multiple date to be called each course
    selected_date = request.form.get('course_date')
    # retrieve order if there is one
    if 'order_id' in session.keys():
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        # order will be None if order_id/session is stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status=False, firstname='', surname='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('Failed trying to create a new order!')
            order = None
    # calculate total price
    total_price = 0
    if order is not None:
        for course in order.courses:
            total_price += course.price
    
    # are we adding an item?
    if courses_id is not None and order is not None:
        course = db.session.scalar(db.select(Course).where(Course.id==courses_id))
        if course not in order.courses:
            try:
                order.courses.append(course)
                db.session.commit()
            except:
                flash('There was an issue adding the item to your basket',category='danger')
            return redirect(url_for('main.order'))
        else:
            flash('There is already one of these in the basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order=order, total_price=total_price,selected_date = selected_date)

# Delete specific basket items
# Note this route cannot accept GET requests now
@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        course_to_delete = db.session.scalar(db.select(Course).where(Course.id==id))
        try:
            order.courses.remove(course_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

# Complete the order
@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = db.get_or_404(Order, session['order_id'])
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.phone = form.phone.data
            total_cost = 0
            for course in order.courses:
                total_cost += course.price
            order.totalcost = total_cost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you for choosing us! Your order is confirmed, See you in park soon')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)
