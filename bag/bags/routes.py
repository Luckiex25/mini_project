from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Bag

bags_bp = Blueprint('bags', __name__, template_folder='templates')

@bags_bp.route('/bags')
@login_required
def index():
    q = request.args.get('q', '')
    if q:
        bags = Bag.query.filter(
            Bag.name.ilike(f'%{q}%'),
            Bag.user_id == current_user.id
        ).all()
    else:
        bags = Bag.query.filter_by(user_id=current_user.id).all()
    return render_template('bags/index.html', bags=bags, search=q)

@bags_bp.route('/bags/new', methods=['GET', 'POST'])
@login_required
def new_bag():
    if request.method == 'POST':
        bag = Bag(
            name=request.form['name'],
            brand=request.form.get('brand', ''),
            description=request.form.get('description', ''),
            price=float(request.form['price']),
            stock=int(request.form.get('stock', 0)),
            image_url=request.form.get('image_url', ''),
            user_id=current_user.id
        )
        db.session.add(bag)
        db.session.commit()
        flash('เพิ่มกระเป๋าสำเร็จ!', 'success')
        return redirect(url_for('bags.index'))
    return render_template('bags/new_bag.html')

@bags_bp.route('/bags/edit/<int:bag_id>', methods=['GET', 'POST'])
@login_required
def edit_bag(bag_id):
    bag = Bag.query.get_or_404(bag_id)
    if request.method == 'POST':
        bag.name        = request.form['name']
        bag.brand       = request.form.get('brand', '')
        bag.description = request.form.get('description', '')
        bag.price       = float(request.form['price'])
        bag.stock       = int(request.form.get('stock', 0))
        bag.image_url   = request.form.get('image_url', '')
        db.session.commit()
        flash('แก้ไขสำเร็จ!', 'success')
        return redirect(url_for('bags.index'))
    return render_template('bags/edit_bag.html', bag=bag)

@bags_bp.route('/bags/delete/<int:bag_id>')
@login_required
def delete_bag(bag_id):
    bag = Bag.query.get_or_404(bag_id)
    db.session.delete(bag)
    db.session.commit()
    flash('ลบสำเร็จ', 'success')
    return redirect(url_for('bags.index'))

@bags_bp.route('/bags/<int:bag_id>')
@login_required
def bag_detail(bag_id):
    bag = Bag.query.get_or_404(bag_id)
    return render_template('bags/bag_detail.html', bag=bag)
