from flask import Flask
from flask import request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from authenticate import auth
import os

app = Flask(__name__)
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dishes.sqlite3'


#create a table dishes in the database
class Dishes(db.Model):

    __tablename__ = 'dishes'

    id = db.Column(
        db.Integer,
        # UUID(as_uuid=True),
        primary_key=True,
        # default=uuid.uuid4,
        unique=True
    )

    dish_name = db.Column(
        db.String(100),
        index=True,
        unique=True,
        nullable=False
    )

    dish_cost = db.Column(
        db.String(100),
        index=True,
        nullable=False
    )

    dish_image=db.Column(
        db.String(100),
        index=True,
        nullable=False)

    def __init__(self,dish_name,dish_cost,dish_image):
      self.dish_name=dish_name
      self.dish_cost=dish_cost
      self.dish_image=dish_image



#This error handler is used to display the   
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#This class is used to serialize all the dishes in our catalog
def menu(dish):
  return {"dishID":dish.id,
      "dishName":dish.dish_name,
      "dishCost":dish.dish_cost,
      "dishImage":dish.dish_image}

# A route to return all of the available dishes in our catalog  
@app.route('/app/v1/resources/dishes', methods=['GET'])
@auth.login_required
def api_all():
    all_dishes=Dishes.query.all()
    all_dishes=list(map(menu,all_dishes))
    return jsonify(all_dishes)
 
# A route to add new dish to the dishes in our catalog 
@app.route('/app/v1/resources/dishes', methods=['POST'])
@auth.login_required
def add_dish():
    dishName = request.form["dishName"]
    dishCost = request.form["dishCost"]
    if request.files:
        dishImage = request.files["dishImage"]
        dishImage.save(os.path.join(dishImage.filename))
    dish=Dishes(dishName,dishCost,dishImage.filename)
    db.session.add(dish)
    db.session.commit()
    return jsonify(dish.id)    


# A route to delete all dishes in our catalog
@app.route('/app/v1/resources/dishes', methods=['DELETE'])
@auth.login_required
def api_delete_all():
    dishes=Dishes.query.all()
    if dishes == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    del_list=[]
    for dish in dishes:
      del_list.append(dish.id)
      db.session.delete(dish)
    db.session.commit()
    return jsonify(del_list)

# A route to display a dish in our catalog with matching dish id
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['GET'])
@auth.login_required
def get_dish(dish_id):  
    dish=Dishes.query.filter_by(id=dish_id).first()
    if dish == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    else:
      return jsonify(menu(dish))




# A route to update a dish in our catalog with matching dish id
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['PUT'])
@auth.login_required
def update_dish(dish_id):
    dish=Dishes.query.filter_by(id=dish_id).first()
    if dish == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    else:
      dishName = request.form["dishName"]
      dish.dish_name=dishName
      dishCost = request.form["dishCost"]
      dish.dish_cost=dishCost
      if "dishImage" in request.files:
        dishImage = request.files["dishImage"]
        dishImage.save(os.path.join(dishImage.filename))
        dish.dish_image=dishImage.filename
      db.session.commit()
      return jsonify(dish_id)

# A route to delete a dish in our catalog with matching dish id
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['DELETE'])
@auth.login_required
def delete_task(dish_id):
    dish=Dishes.query.filter_by(id=dish_id).first()
    if dish == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    else:
      dish_id=dish.id
      db.session.delete(dish)
      db.session.commit()
      return jsonify(dish_id)

# A route to update partial entries of a dish in our catalog with matching dish id
@app.route('/app/v1/resources/dishes/<int:dish_id>', methods=['PATCH'])
@auth.login_required
def patch_dish(dish_id):
    dish=Dishes.query.filter_by(id=dish_id).first()
    if dish == None:
      return make_response(jsonify({'error': 'No dish'}), 400)
    else:
      if "dishName" in request.form:
        dish.dish_name=request.form["dishName"]
      if "dishCost" in request.form:
        dish.dish_cost=request.form["dishCost"]  
      if "dishImage" in request.files:
        dishImage = request.files["dishImage"]
        dishImage.save(os.path.join(dishImage.filename))
        dish.dish_image=dishImage.filename
      db.session.commit()
      return jsonify(dish_id)
  


if __name__ == "__main__":
	db.create_all()
	app.run()