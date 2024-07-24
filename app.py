from flask import Flask, request
from copy import copy
import sqlite3

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_from_db(query, params, many=True):
    con = sqlite3.connect('db')
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(query, (params,))
    if many:
        res = cur.fetchall()
    else:
        res = cur.fetchone()
    con.close()
    return (res)


def insert_to_db(query, params):
    con = sqlite3.connect('db')
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    con.close()


@app.post('/register')
def new_user_register():
    form_data = request.form
    query = '''
    INSERT INTO user (login, password, birth_date, phone) 
    VALUES (?, ?, ?, ? )
    '''
    params = (
        form_data["login"],
        hash(form_data["password"]),
        form_data["birth_date"],
        form_data["phone"]
    )
    insert_to_db(query, params)
    return 'new user register'


@app.get('/register')
def user_register_invitation():
    return f"""<form action="/register" method="post"">
  <label for="login">login:</label><br>
  <input type="text" id="login" name="login"><br>
  <label for="password">password:</label><br>
  <input type="password" id="password" name="password">
  <label for="birth_date">birth_date:</label><br>
  <input type="date" id="birth_date" name="birth_date">
  <label for="phone">phone:</label><br>
  <input type="text" id="phone" name="phone">
  
  <input type="submit" value="Submit">
</form>"""
    
   

@app.post('/login')
def user_login():
    return 'new user loggen in'


@app.get('/login')
def user_login_form():
    return 'please enter credentials'


@app.post('/user')
def new_user():
    return 'user data has been created'

# ('select login, phone, birth_date from user where id=1')
@app.get('/user/<int:user_id>')
def user_info(user_id):
    query = ''' SELECT login, phone, birth_date FROM user where id=? '''
    params = user_id
    res = get_from_db(query,params)
    return res


@app.put('/user')
def user_editing():
    return 'user information edited'


@app.post('/funds')
def add_funds():
    return 'account financing'


@app.get('/funds/<int:user_id>')
def deposit_info(user_id):
    query = '''select funds  from user where id=? '''
    params = user_id
    res = get_from_db(query,params)
    return res


@app.post('/reservation')
def reservations_service():
    return 'data  reservations'


@app.get('/reservation/<int:user_id>')
def data_reservation(user_id):
    query = '''select * from reservation where user_id=? '''
    params = user_id
    res = get_from_db(query, params)
    return res


@app.post('/checkout')
def user_checkout():
    return 'payment verification'


@app.get('/checkout')
def checkout_info():
    return 'receiving a transfer'


@app.put('/checkout')
def edit_checkout():
    return 'edit sum'


@app.get('/fitness_center<int:gym_id>')
def user_fitness_center(gym_id):
    query = '''select * from fitness_center where id=? '''
    params = gym_id
    res = get_from_db(query,params)
    return res


@app.get('/fitness_center/<gym_id>/services/<service_id>')
def get_service_info(gym_id, service_id):
    return f'fitness center {gym_id} service {service_id} info'


@app.get('/fitness_center/<int:gym_id>/service')                  #+
def get_service(gym_id):
    query = ''' select * from service where id=? '''
    params = gym_id
    res = get_from_db(query, params)
    return res


@app.get('/user/reservation/<int:reservation_id>')                #+
def reservation_info(reservation_id):
    query = '''select * from reservation where id=? '''
    params = reservation_id
    res = get_from_db(query, params)
    return res



@app.put('/user/reservation/<reservation_id>')
def reservation_edit_info(reservation_id):
    return f'user reservations {reservation_id} edit'


@app.delete('/user/reservation/<reservation_id>')
def delete_info_reservation(reservation_id):
    return f'user reservations {reservation_id} delete'


@app.get('/fitness_center/<gym_id>')
def fitness_center_info(gym_id):
    query = ''' select * from fitness_center where id=? '''
    params = gym_id
    res = get_from_db(query, params)
    return res

@app.get('/fitness_center/<gym_id>/coach')
def get_coach(gym_id):
    query = '''select * from coach where gym_id=? '''
    params = gym_id
    res = get_from_db(query, params)
    return res



@app.get('/fitness_center/<int:gym_id>/coach/<int:coach_id>')
def get_coach_info(gym_id, coach_id):
    query = '''select * from coach where id=? '''
    query2 = '''select * from fitness_center where id=? '''
    params1 = coach_id
    params2 = gym_id
    res1 = get_from_db(query, params1)
    res2 = get_from_db(query2, params2)
    respons = res1 + res2
    return respons



@app.get('/fitness_center/<gym_id>/coach/<coach_id>/rating')
def get_coach_rating(gym_id, coach_id):
    guery = '''select * from coach where id=? '''
    query2 = '''select * from fitness_center where id=? '''
    query3 = '''select * from rating where id=? '''
    params1 = coach_id
    params2 = gym_id
    params3 = coach_id
    res = get_from_db(query2, params1)
    res2 = get_from_db(query3, params2)
    res3 = get_from_db(query3, params3)
    respons = res + res2 + res3
    return respons


@app.post('/fitness_center/<gym_id>/coach/<coach_id>/rating')
def set_coach_rating(gym_id, coach_id):
    return f'fitness center {gym_id} coach {coach_id} rating was added'


@app.put('/fitness_center/<gym_id>/trainer/<coach_id>/rating')
def update_coach_rating(gym_id, coach_id):
    return f'fitness center {gym_id} trainer {coach_id} rating was updated'


@app.get('/fitness_center/{gym_id}/loyality_programs')
def user_loyality_programs(gym_id: int):
    query = '''select * from loyality_programs where id=? '''
    params = gym_id
    res = get_from_db(query, params)
    return res





if __name__ == '  main  ':
    app.run()
