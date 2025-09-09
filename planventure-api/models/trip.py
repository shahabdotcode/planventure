from datetime import datetime
from . import db
import json

def generate_default_itinerary(start_date, end_date):
    """
    Generate a default itinerary template based on trip duration.
    
    Args:
        start_date (datetime): Trip start date
        end_date (datetime): Trip end date
        
    Returns:
        dict: A structured itinerary template with days and default activities
    """
    if not start_date or not end_date:
        return {"day1": {"activities": []}}
        
    # Calculate trip duration in days
    trip_duration = (end_date - start_date).days + 1
    
    # Ensure at least one day
    trip_duration = max(1, trip_duration)
    
    itinerary = {}
    
    for day in range(1, trip_duration + 1):
        day_key = f"day{day}"
        
        # Create template activities for each day
        morning_activity = {
            "time": "09:00",
            "activity": f"Morning activity for day {day}",
            "location": "To be determined"
        }
        
        lunch = {
            "time": "13:00",
            "activity": "Lunch",
            "location": "To be determined"
        }
        
        afternoon_activity = {
            "time": "15:00",
            "activity": f"Afternoon activity for day {day}",
            "location": "To be determined"
        }
        
        dinner = {
            "time": "19:00",
            "activity": "Dinner",
            "location": "To be determined"
        }
        
        itinerary[day_key] = {
            "activities": [morning_activity, lunch, afternoon_activity, dinner]
        }
    
    return itinerary

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    coordinates = db.Column(db.Text)  # Store JSON as Text for SQLite compatibility
    itinerary = db.Column(db.Text)    # Store JSON as Text for SQLite compatibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref=db.backref('trips', lazy=True))

    def __repr__(self):
        return f'<Trip {self.destination}>'
        
    def set_coordinates(self, coordinates_dict):
        """Convert dictionary to JSON string for storage"""
        if coordinates_dict is not None:
            self.coordinates = json.dumps(coordinates_dict)
        else:
            self.coordinates = None
            
    def set_itinerary(self, itinerary_dict):
        """Convert dictionary to JSON string for storage"""
        if itinerary_dict is not None:
            self.itinerary = json.dumps(itinerary_dict)
        else:
            # If no itinerary provided, create a default one based on trip dates
            if self.start_date and self.end_date:
                default_itinerary = generate_default_itinerary(self.start_date, self.end_date)
                self.itinerary = json.dumps(default_itinerary)
            else:
                # Fallback to an empty day template if no dates
                self.itinerary = json.dumps({"day1": {"activities": []}})

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'destination': self.destination,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'coordinates': json.loads(self.coordinates) if self.coordinates else None,
            'itinerary': json.loads(self.itinerary) if self.itinerary else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def generate_default_itinerary(start_date, end_date):
        """
        Generate a default itinerary template based on trip duration.
        
        Args:
            start_date (datetime): Trip start date
            end_date (datetime): Trip end date
            
        Returns:
            dict: A structured itinerary template with days and default activities
        """
        if not start_date or not end_date:
            return {"day1": {"activities": []}}
            
        # Calculate trip duration in days
        trip_duration = (end_date - start_date).days + 1
        
        # Ensure at least one day
        trip_duration = max(1, trip_duration)
        
        itinerary = {}
        
        for day in range(1, trip_duration + 1):
            day_key = f"day{day}"
            
            # Create template activities for each day
            morning_activity = {
                "time": "09:00",
                "activity": f"Morning activity for day {day}",
                "location": "To be determined"
            }
            
            lunch = {
                "time": "13:00",
                "activity": "Lunch",
                "location": "To be determined"
            }
            
            afternoon_activity = {
                "time": "15:00",
                "activity": f"Afternoon activity for day {day}",
                "location": "To be determined"
            }
            
            dinner = {
                "time": "19:00",
                "activity": "Dinner",
                "location": "To be determined"
            }
            
            itinerary[day_key] = {
                "activities": [morning_activity, lunch, afternoon_activity, dinner]
            }
        
        return itinerary
