from flask import Blueprint, request, jsonify
from models import db
from models.trip import Trip
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

trips_bp = Blueprint('trips', __name__, url_prefix='/api/trips')

@trips_bp.route('', methods=['POST'])  # Empty string for root of the prefix
@jwt_required()
def create_trip():
    current_user_id = get_jwt_identity()
    try:
        data = request.get_json()
        
        if not data or not data.get('destination'):
            return jsonify({'error': 'Destination is required'}), 400
            
        # Parse dates from request
        start_date = datetime.fromisoformat(data.get('start_date')) if data.get('start_date') else None
        end_date = datetime.fromisoformat(data.get('end_date')) if data.get('end_date') else None
        
        trip = Trip(
            user_id=current_user_id,
            destination=data['destination'],
            start_date=start_date,
            end_date=end_date
        )
        
        # Handle coordinates
        trip.set_coordinates(data.get('coordinates'))
        
        # Set itinerary - default will be generated if none provided
        trip.set_itinerary(data.get('itinerary'))
        
        db.session.add(trip)
        db.session.commit()
        
        return jsonify({
            'message': 'Trip created successfully',
            'trip': trip.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@trips_bp.route('', methods=['GET'])  # Empty string for root of the prefix
@jwt_required()  # Ensure this decorator is used
def get_trips():
    current_user_id = get_jwt_identity()
    
    # Ensure user_id is properly handled
    if not current_user_id:
        return jsonify({"message": "Authentication required"}), 401
        
    try:
        trips = Trip.query.filter_by(user_id=current_user_id).all()
        return jsonify({
            'trips': [trip.to_dict() for trip in trips]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    current_user_id = get_jwt_identity()
    try:
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user_id).first()
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        return jsonify(trip.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    current_user_id = get_jwt_identity()
    try:
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user_id).first()
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
            
        data = request.get_json()
        
        if 'destination' in data:
            trip.destination = data['destination']
        if 'start_date' in data:
            trip.start_date = datetime.fromisoformat(data['start_date'])
        if 'end_date' in data:
            trip.end_date = datetime.fromisoformat(data['end_date'])
        if 'coordinates' in data:
            trip.set_coordinates(data['coordinates'])
        if 'itinerary' in data:
            trip.set_itinerary(data['itinerary'])
            
        db.session.commit()
        
        return jsonify({
            'message': 'Trip updated successfully',
            'trip': trip.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    current_user_id = get_jwt_identity()
    try:
        trip = Trip.query.filter_by(id=trip_id, user_id=current_user_id).first()
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
            
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({
            'message': 'Trip deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
