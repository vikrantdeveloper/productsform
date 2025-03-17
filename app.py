# -*- coding: utf-8 -*-
"""
Created on March 16 12:02:51 2020

@author: Vikrant
"""

from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask import Response,send_file

app = Flask(__name__)

import rds_db as db
import boto3

app.secret_key = b'shv\x04@U\x90\xbeJf\xda\x0f\x9bF\x9aK\x1e\x831\x98\xf0\xc4$\x82'

# AWS RDS Credentials
AWS_ACCESS_KEY = "AKIA5G2VGMRHFYHTFIOR"
AWS_SECRET_KEY = "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"
RDS_INSTANCE_ID = "productsdb"

# Initialize AWS RDS Client
rds_client = boto3.client(
    'rds',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='eu-north-1'
)

@app.route("/backup", methods=["GET"])
def create_backup():
    """Creates a manual snapshot of the RDS database"""
    snapshot_id = f"{RDS_INSTANCE_ID}-backup"
    try:
        rds_client.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_id,
            DBInstanceIdentifier=RDS_INSTANCE_ID
        )
        flash("Database backup created successfully!", "success")
    except Exception as e:
        flash(f"Backup failed: {e}", "danger")

    return redirect(url_for("index"))

@app.route("/restore", methods=["GET"])
def restore_backup():
    """Restores the database from the latest snapshot"""
    snapshot_id = f"{RDS_INSTANCE_ID}-backup"
    try:
        rds_client.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=RDS_INSTANCE_ID,
            DBSnapshotIdentifier=snapshot_id
        )
        flash("Database restored successfully!", "success")
    except Exception as e:
        flash(f"Restore failed: {e}", "danger")

    return redirect(url_for("index"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jinsert',methods = ['post'])
def jinsert():
    
    if request.method == 'POST':
        product_id = request.form['id']
        description = request.form['description']
        price = request.form['price']
        db.add_product(product_id, description, price)
        details = db.list_product()
        print(details)
        return render_template('index.html',var=details)

@app.route('/finsert', methods=['POST'])
def finsert():
    if request.method == 'POST':
        product_id = request.form['id']
        description = request.form['description']
        price = request.form['price']
        
        db.add_product(product_id, description, price)  # Insert data
        
        return redirect(url_for('index'))  # Refresh page with updated data
 
@app.route('/delete_all', methods=['POST'])
def delete_all():
    db.delete_all_products()
    flash("All products have been deleted successfully!", "success")  # Flash success message
    return redirect(url_for('index'))  # Refresh the page after deletion
   
if __name__ == "__main__":
    app.run(debug=True)