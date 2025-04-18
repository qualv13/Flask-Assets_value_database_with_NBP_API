from datetime import date, datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import secrets
import requests
from base import db, Rate, Asset  #dalej też konkretne obiekty
from sqlalchemy import update, desc, or_, engine

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

currency_url = 'https://api.nbp.pl/api/exchangerates/tables/a/last/1/'  #'https://api.nbp.pl/api/exchangerates/rates/c/usd/today/'

with app.app_context():
    db.create_all()


def get_todays_rates():
    yesterday = datetime.today().date() - timedelta(days=1)
    end = datetime.combine(datetime.today().date(), datetime.max.time())
    start = datetime.combine(yesterday, datetime.max.time())

    latest_rates = db.session.execute(
        db.select(Rate).filter(Rate.date.between(start, end))
    ).scalars().all()
    if latest_rates:
        print("Yesterday's rates already exist in the database.")
        return {
            'effectiveDate': yesterday.strftime('%Y-%m-%d'),
            'rates': [
                {
                    'code': rate.code,
                    'currency': rate.currency,
                    'mid': rate.rate
                } for rate in latest_rates
            ]
        }

    response = requests.get(currency_url)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return

    data = response.json()[0]
    rate_date = datetime.strptime(data['effectiveDate'], '%Y-%m-%d')

    for rate in data['rates']:
        new_rate = Rate(
            code=rate['code'],
            currency=rate['currency'],
            rate=rate['mid'],
            date=rate_date
        )
        db.session.add(new_rate)
    db.session.commit()
    return data


@app.route('/')
def home():
    return render_template('index.html', responses=get_todays_rates())


@app.route("/assets")
def asset_list():
    search = request.args.get("search", "", type=str)
    sort_by = request.args.get("sort", "name", type=str)
    order = request.args.get("order", "asc", type=str)
    page = request.args.get("page", 1, type=int)

    query = db.select(Asset)
    if search:
        query = query.filter(
            or_(
                Asset.name.ilike(f"%{search}%"),
                Asset.currency.ilike(f"%{search}%")
            )
        )

    sort_column = getattr(Asset, sort_by, Asset.name)
    if order == "desc":
        sort_column = sort_column.desc()

    query = query.order_by(sort_column)
    assets_paginated = db.paginate(query, page=page, per_page=5, error_out=False)

    latest_date = db.session.execute(
        db.select(Rate.date).order_by(desc(Rate.date))
    ).scalars().first()

    rate_map = {}
    if latest_date:
        rates = db.session.execute(
            db.select(Rate).filter(Rate.date == latest_date)
        ).scalars().all()
        rate_map = {rate.code: rate.rate for rate in rates}

    asset_data = []
    for asset in assets_paginated.items:
        pln_value = asset.value
        if not asset.is_pln:
            rate = rate_map.get(asset.currency)
            if rate:
                pln_value = round(asset.value * rate, 2)
            elif asset.currency == "":
                pln_value = "Missing code"
            else:
                pln_value = 'Wrong code'
        asset_data.append((asset, pln_value))

    return render_template('asset/list.html',
                           assets=asset_data,
                           pagination=assets_paginated,
                           search=search,
                           sort=sort_by,
                           order=order)


@app.route("/assets/create", methods=["GET", "POST"])
def asset_create():
    if request.method == "POST":
        asset = Asset(
            name=request.form['name'],
            value=request.form['value'],
            currency=request.form['currency']
        )
        if not asset.name or not asset.value:
            flash('Please input name and value.', 'alert')
            return render_template("asset/create.html")
        if asset.currency is None:
            asset.currency = 'PLN'
        if asset.currency == 'PLN':
            asset.is_pln = True
        asset.value = float(asset.value)
        db.session.add(asset)
        db.session.commit()
        return redirect(url_for("asset_detail", id=asset.id))

    return render_template("asset/create.html")


@app.route("/asset/<int:id>", methods=["GET", "POST"])
def asset_detail(id):
    asset = db.get_or_404(Asset, id)
    if request.method == "POST":
        return redirect(url_for("asset_list"))
    return render_template("asset/detail.html", asset=asset)


@app.route("/asset/<int:id>/edit", methods=["GET", "POST"])
def asset_edit(id):
    asset = db.get_or_404(Asset, id)
    if request.method == "POST":
        new_asset = Asset(
            name=request.form['name'],
            value=request.form['value'],
            currency=request.form['currency']
        )
        if new_asset.name is not None:
            asset.name = new_asset.name
        if asset.value is not None:
            asset.value = float(new_asset.value)
        if new_asset.currency is not None:
            asset.currency = new_asset.currency
        asset.is_pln = (asset.currency == 'PLN')
        db.session.commit()
        flash('Values updated.', 'info')
        return redirect(url_for("asset_list"))
    return render_template("asset/edit.html", asset=asset)


@app.route("/asset/<int:id>/delete", methods=["GET", "POST"])
def asset_delete(id):
    asset = db.get_or_404(Asset, id)
    return render_template("asset/delete.html", asset=asset)


@app.route("/asset/<int:id>/delete/confirm", methods=["GET", "POST"])
def asset_delete_confirm(id):
    asset = db.get_or_404(Asset, id)
    if request.method == "POST":
        db.session.delete(asset)
        db.session.commit()
        return redirect(url_for("asset_list"))
    return render_template("asset/delete.html", asset=asset)


if __name__ == '__main__':
    app.run()
