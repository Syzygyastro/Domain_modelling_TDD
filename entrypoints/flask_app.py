from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import domain.model as model
import adapters.orm as orm
import service_layer.services as services
import adapters.repository as repository



orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgress_uri()))
app = Flask(__name__)

@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlRespository(session)
    
    line = model.OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty']
    )
    
    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({'message' : str(e)}), 400
        
    return jsonify({'batchref' : batchref}), 201



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


    
    