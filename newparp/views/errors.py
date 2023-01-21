import traceback

from flask import render_template, request, g, jsonify, current_app


def error_403(e):
    return render_template("errors/403.html"), 403


def error_404(e):
    return render_template("errors/404.html"), 404


def error_500(e):
    if "sentry" in current_app.extensions:
        current_app.extensions["sentry"].captureException()

    exception = traceback.format_exc()

    if hasattr(g, "user") and g.user:
        admin = g.user.is_admin
    else:
        admin = False

    if request.accept_mimetypes.accept_json:
        if not admin:
            raise
        elif "debug" in request.args or "debug" in request.form:
            return jsonify({"error": exception}), 500
        else:
            raise

    return render_template("errors/500.html",
        exception=exception,
        admin=admin
    ), 500

