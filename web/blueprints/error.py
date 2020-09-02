
from flask import (
    Blueprint, render_template)

from werkzeug.exceptions import (
    BadRequest, NotFound, MethodNotAllowed, RequestTimeout, InternalServerError, BadGateway, ServiceUnavailable)

from app import db

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
