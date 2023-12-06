#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():

    # Delete existing messages from the database
    Message.query.delete()

    messages = []

    for i in range(20):
        # Create a new message with a random body and username
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    # Add all the new messages to the database and commit the transaction
    db.session.add_all(messages)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        make_messages()
