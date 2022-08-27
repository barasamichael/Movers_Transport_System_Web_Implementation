import faker
from random import randint
from . import db
from .models import (loader, driver, vehicle, vehicle_make, good, member, service, 
        offence, offender)
from sqlalchemy.exc import IntegrityError

def loaders(count = 50):
    fake = faker.Faker()
    i = 1
    while i <= count:
        if randint(1, 10) % 2 == 0:
            gender = 'male'
        else:
            gender = 'female'

        name = fake.name()
        name_list = name.split()

        l_loader = loader(
                first_name = name_list[0],
                last_name = name_list[0],
                middle_name = name_list[1],
                gender = gender,
                date_of_birth = fake.date_of_birth(),
                residential_address = fake.street_address(),
                email_address = fake.email(),
                phone_no = fake.phone_number()
                )
        db.session.add(l_loader)
        try:
            db.session.commit()
            i += 1
            print('saving loader #{}...'.format(i))
        except IntegrityError:
            db.session.rollback()

    print('Done')


def drivers(count = 17):
    fake = faker.Faker()
    i = 1
    while i <= count:
        if randint(1, 10) % 2 == 0:
            gender = 'male'
        else:
            gender = 'female'

        name = fake.name()
        name_list = name.split()

        d_driver= driver(
                first_name = name_list[0],
                last_name = name_list[0],
                middle_name = name_list[1],
                gender = gender,
                date_of_birth = fake.date_of_birth(),
                residential_address = fake.street_address(),
                email_address = fake.email(),
                phone_no = fake.phone_number()
                )
        db.session.add(d_driver)
        try:
            db.session.commit()
            i += 1
            print('saving driver #{}...'.format(i))
        except IntegrityError:
            db.session.rollback()

    print('Done')

def vehicles():
    data = ['KBC 6356H', 'KBY 7474U', 'KBC 9776K', 'KDA 8478I', 'KBC 7686M', 'KAD 7653H', 'KCD 7367J', 'KDA 8633D', 'KBS 8503V', 'KBA 8637A', 'KDE 7476K', 'KBC 8479E']

    for i in data:
        v_vehicle = vehicle(
                plate_no = i,
                make_id = randint(1, 4)
                )
        db.session.add(v_vehicle)
        try:
            db.session.commit()
            print('Saved {} ...'.format(i))
        except IntegrityError:
            db.session.rollback()
        
    print('Done')


def vehicle_makes():
    data = [
            ('Pickup', 1, 200, 2, 200, 2000 ),
            ('Lorry', 7, 650, 6, 300, 3000),
            ('Trailer', 12, 1500, 10, 500, 8000),
            ('Refrigerated truck', 3, 1000, 4, 450, 5000)
            ]

    for i in data:
        make = vehicle_make(
                make_type = i[0],
                capacity = i[1],
                cost_per_km = i[2],
                no_of_loaders = i[3],
                loader_payment = i[4],
                driver_payment = i[5]
                )

        db.session.add(make)
        try:
            db.session.commit()
            print('saving...')
        except IntegrityError:
            db.session.rollback()

    print('done')

def offences():
    data = [
            'over speeding',
            'driving while drunk',
            'over loading',
            'causing perishable goods to be spoiled due to misconduct \
                    during delivery'
            ]

    for i in data:
        offense = offence(description = i)
        db.session.add(offense)
        try:
            db.session.commit()
            print('Saving...')
        except IntegrityError:
            db.session.rollback()
        
    print('done')


def members():
    pass
