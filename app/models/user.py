# SBU/app/models/user.py
from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey, DateTime, Text


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    bots = relationship('Bot', backref='user')
    conversation_settings = relationship('ConversationSetting', backref='user')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Bot(db.Model):
    __tablename__ = 'bots'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(f'{add_prefix_for_prod("users")}.id'), nullable=False)
    settings = db.Column(JSON)

    transcripts = relationship('Transcript', backref='bot')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'settings': self.settings,
        }


class ConversationSetting(db.Model):
    __tablename__ = 'conversation_settings'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(f'{add_prefix_for_prod("users")}.id'), nullable=False)
    setting_details = db.Column(JSON)

    debates = relationship('Debate', backref='conversation_setting')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'setting_details': self.setting_details,
        }


class Debate(db.Model):
    __tablename__ = 'debates'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    conversation_setting_id = db.Column(db.Integer, ForeignKey(f'{add_prefix_for_prod("conversation_settings")}.id'), nullable=False)
    initiator_bot_id = db.Column(db.Integer, ForeignKey(f'{add_prefix_for_prod("bots")}.id'), nullable=False)
    opponent_bot_id = db.Column(db.Integer, ForeignKey(f'{add_prefix_for_prod("bots")}.id'), nullable=False)
    start_time = db.Column(DateTime)
    end_time = db.Column(DateTime)
    topic = db.Column(db.String(255))
    result = db.Column(db.String(255))

    transcripts = relationship('Transcript', backref='debate')

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_setting_id': self.conversation_setting_id,
            'initiator_bot_id': self.initiator_bot_id,
            'opponent_bot_id': self.opponent_bot_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'topic': self.topic,
            'result': self.result,
        }


class Transcript(db.Model):
    __tablename__ = 'transcripts'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    debate_id = db.Column(db.Integer, ForeignKey(f'{add_prefix_for_prod("debates")}.id'), nullable=False)
    bot_id = db.Column(db.Integer, ForeignKey(f'{add_prefix_for_prod("bots")}.id'), nullable=False)
    message = db.Column(Text)
    time = db.Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'debate_id': self.debate_id,
            'bot_id': self.bot_id,
            'message': self.message,
            'time': self.time.isoformat() if self.time else None,
        }