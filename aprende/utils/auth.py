"""The authentication state."""
import reflex as rx
from ..repository.connect_db import connect
from sqlmodel import Session, select

from .base import State, User


class AuthState(State):
    """The authentication state for sign up and login page."""

    username: str
    password: str
    confirm_password: str

    def signup(self):
        """Sign up a user."""
        engine = connect()
        with Session(engine) as session:
            if self.password != self.confirm_password:
                return rx.window_alert("Contraseña Incorrecta.")
            if session.exec(select(User).where(User.username == self.username)).first():
                return rx.window_alert("Usuario ya existente.")
            self.user = User(username=self.username, password=self.password)
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        """Log in a user."""
        engine = connect()
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.username == self.username)
            ).first()
            if user and user.password == self.password:
                self.user = user
                return rx.redirect("/")
            else:
                return rx.window_alert("Invalid usuario or contrasena.")