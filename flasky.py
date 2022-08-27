import os
from app import create_app, db
from flask_migrate import Migrate

from app.models import (vehicle_make, small_scale_farmer, loader, driver, user, 
        vehicle, offence, offender, good, service, member, good_assignment, order, 
        Permission, role)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db = db, vehicle_make = vehicle_make, 
            small_scale_farmer = small_scale_farmer, loader = loader, 
            driver = driver, vehicle = vehicle, offence = offence, 
            offender = offender, good = good, service = service, member = member, 
            good_assignmnent = good_assignment, order = order, user = user, 
            Permission = Permission, role = role
            )

if __name__ == '__main__':
    app.run()
