from flask import Flask, render_template, request, abort, redirect, url_for
from db_connect import get_connection


app = Flask(__name__)

@app.route('/', methods =['GET', 'POST'])
def index():
    conn = get_connection()
    if request.method=='POST':
        patient_name = request.form.get('patient_name')
        patient_age = request.form.get('patient_age')
        patient_email = request.form.get('patient_email')
        values = (patient_name, patient_age, patient_email)
        with conn.cursor() as cur:
            sql_ptmt = "insert into patient(Name, age, email_id ) values(?,?,?)"
            cur.execute(sql_ptmt, values)
            conn.commit()
    with conn.cursor() as cur:
        sql_ptmt = "select * from patient"
        cur.execute(sql_ptmt)
        res = cur.fetchall()
    conn.close()
    return render_template('index.html', patient = res)

@app.route("/patient/<int:patient_id>")
def get_patient(patient_id):
    conn = get_connection()
    with conn.cursor() as cur:
        sql_ptmt = "select * from patient where patient_id = ?"
        cur.execute(sql_ptmt, (patient_id,))
        res = cur.fetchone()
    conn.close()
    if res is None:
        abort(404)
    return render_template('patient_detail.html', patient = res)

@app.route("/delete/<int:patient_id>")   
def delete_patient(patient_id):
    conn = get_connection()   
    with conn.cursor() as cur:
        sql_ptmt = "Delete from patient where patient_id=?"
        cur.execute(sql_ptmt,(patient_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route("/edit/<int:patient_id>", methods = ['GET', 'POST'])
def edit_patient(patient_id):
    conn = get_connection()
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        patient_age = request.form.get('patient_age')
        patient_email = request.form.get('patient_email')
        with conn.cursor() as cur:
            cur.execute( """update patient
                        set Name = ?, Age =?, email_id = ? where patient_id = ? """,
                        (patient_name, patient_age, patient_email, patient_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    with conn.cursor() as cur:
        sql_ptmt = "select * from patient where patient_id = ?"
        cur.execute(sql_ptmt, (patient_id, ))
        res = cur.fetchone()
    if res:
        return render_template('update_patient.html', patient=res)
    else:
            abort(404)
if __name__ == "__main__":
    app.run(debug=True)