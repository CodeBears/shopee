from sqlalchemy import or_
from app import db
from orm.models import User
from utils.auth_tool import AuthTool
from utils.const import Const
from utils.db_tool import DBTool
from utils.error_code import ErrorCode
from utils.errors import ValidationError


class MemberHandler:
    @staticmethod
    def sign_in(email, password):
        member = User.query.filter(
            User.email == email,
        ).first()
        if not member or not AuthTool.check_password(password, hashed=member.password):
            raise ValidationError(error_code=ErrorCode.EMAIL_OR_PASSWORD_WRONG)
        res = {
            'email': member.email,
            'username': member.username,
            'role': member.role,
            'is_valid': member.is_valid,
        }
        res['access_token'] = AuthTool.get_access_token(**res)
        return res

    @staticmethod
    def sign_up(email, username, password):
        member = User.query.filter(
            or_(
                User.email == email,
                User.username == username
            )
        ).first()
        if member:
            raise ValidationError(error_code=ErrorCode.MEMBER_IS_EXIST)
        member = User(
            email=email,
            username=username,
            password=AuthTool.hash_password(password=password),
            role=Const.Role.MEMBER
        )
        db.session.add(member)
        DBTool.commit()
        res = {
            'email': member.email,
            'username': member.username,
            'role': member.role,
            'is_valid': member.is_valid,
        }
        res['access_token'] = AuthTool.get_access_token(**res)
        return res
