from app import db
from flask import Blueprint
from flask import render_template
from werkzeug.exceptions import BadGateway
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import RequestTimeout
from werkzeug.exceptions import ServiceUnavailable

bp = Blueprint('error', __name__)


@bp.app_errorhandler(NotFound)
@bp.app_errorhandler(BadRequest)
@bp.app_errorhandler(BadGateway)
@bp.app_errorhandler(RequestTimeout)
@bp.app_errorhandler(MethodNotAllowed)
@bp.app_errorhandler(ServiceUnavailable)
@bp.app_errorhandler(InternalServerError)
def handle_exception(e):
    """generic error page"""
    if e.code == 500:
        db.session.rollback()
    return render_template('error/generic.html', e=e), e.code
