import json

from flask import abort, g, make_response, redirect, render_template, request, url_for
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from newparp.helpers.auth import permission_required
from newparp.helpers.characters import validate_character_form
from newparp.model import case_options, Character, Fandom, SearchCharacterGroup, SearchCharacter, SearchCharacterChoice, User
from newparp.model.connections import use_db, db_connect


def search_character_query(id):
    try:
        return g.db.query(SearchCharacter).filter(SearchCharacter.id == id).one()
    except:
        abort(404)


@use_db
@permission_required("search_characters")
def search_character_list():
    return render_template(
        "search_characters/search_character_list.html",
        fandoms=(
            g.db.query(Fandom)
            .order_by(Fandom.name)
            .options(
                joinedload(Fandom.groups)
                .joinedload(SearchCharacterGroup.characters)
            ).all()
        )
    )


@use_db
@permission_required("search_characters")
def new_fandom_post():
    name = request.form["name"].strip()[:100]
    if len(name) == 0:
        abort(400)
    g.db.add(Fandom(name=name))
    return redirect(url_for("rp_search_character_list"))


@use_db
@permission_required("search_characters")
def new_search_character_group_post():
    name = request.form["name"].strip()[:100]
    if len(name) == 0:
        abort(400)

    try:
        fandom = g.db.query(Fandom).filter(Fandom.id == int(request.form["fandom_id"])).one()
    except (ValueError, NoResultFound):
        abort(404)

    order = (
        g.db.query(func.max(SearchCharacterGroup.order))
        .filter(SearchCharacterGroup.fandom_id == fandom.id)
        .scalar() or 0
    ) + 1
    g.db.add(SearchCharacterGroup(fandom_id=fandom.id, name=name, order=order))

    return redirect(url_for("rp_search_character_list"))


@use_db
@permission_required("search_characters")
def new_search_character_get():
    fandoms = g.db.query(Fandom).order_by(Fandom.name).options(joinedload(Fandom.groups)).all()

    character_defaults = {_.name: _.default.arg for _ in SearchCharacter.__table__.columns if _.default}

    return render_template(
        "search_characters/search_character.html",
        character=character_defaults,
        replacements=[],
        regexes=[],
        fandoms=fandoms,
        case_options=case_options,
    )


@use_db
@permission_required("search_characters")
def new_search_character_post():
    new_details = validate_character_form(request.form)
    del new_details["search_character_id"]
    del new_details["shortcut"]
    try:
        group = g.db.query(SearchCharacterGroup).filter(
            SearchCharacterGroup.id == request.form["group_id"],
        ).one()
    except NoResultFound:
        abort(404)
    order = (
        g.db.query(func.max(SearchCharacter.order))
        .filter(SearchCharacter.group_id == group.id)
        .scalar() or 0
    ) + 1
    new_search_character = SearchCharacter(
        group_id=group.id,
        order=order,
        text_preview=request.form.get("text_preview", SearchCharacter.text_preview.default.arg),
        **new_details
    )
    g.db.add(new_search_character)
    return redirect(url_for("rp_search_character_list"))


@use_db
@permission_required("search_characters")
def search_character(id):
    character = search_character_query(id)
    return render_template(
        "search_characters/search_character.html",
        character=character,
        replacements=json.loads(character.replacements),
        regexes=json.loads(character.regexes),
        case_options=case_options,
    )


def search_character_json(id):

    character_json = g.redis.get("search_character:%s" % id)

    if character_json is None:
        db_connect()
        character = search_character_query(id)
        character_json = json.dumps(character.to_dict(include_options=True))
        g.redis.set("search_character:%s" % id, character_json)
        g.redis.expire("search_character:%s" % id, 3600)

    resp = make_response(character_json)
    resp.headers["Content-type"] = "application/json"
    return resp


@use_db
@permission_required("search_characters")
def save_search_character(id):
    character = search_character_query(id)
    new_details = validate_character_form(request.form)
    # Ignore a blank title.
    if new_details["title"] != "":
        character.title = new_details["title"]
    character.name = new_details["name"]
    character.acronym = new_details["acronym"]
    character.color = new_details["color"]
    character.quirk_prefix = new_details["quirk_prefix"]
    character.quirk_suffix = new_details["quirk_suffix"]
    character.case = new_details["case"]
    character.replacements = new_details["replacements"]
    character.regexes = new_details["regexes"]
    character.text_preview = request.form["text_preview"]
    # Remember to clear the cache
    g.redis.delete("search_character:%s" % id)
    return redirect(url_for("rp_search_character_list"))


@use_db
@permission_required("search_characters")
def delete_search_character_get(id):
    # Anon/other is the default character so it can't be deleted.
    if id == 1:
        abort(404)
    character = search_character_query(id)
    return render_template("search_characters/delete_search_character.html", character=character)


@use_db
@permission_required("search_characters")
def delete_search_character_post(id):
    # Anon/other is the default character so it can't be deleted.
    if id == 1:
        abort(404)
    character = search_character_query(id)
    # Set all references to anon/other first.
    g.db.query(User).filter(User.roulette_search_character_id == character.id).update({
        "roulette_search_character_id": 1,
    })
    g.db.query(User).filter(User.search_character_id == character.id).update({
        "search_character_id": 1,
    })
    g.db.query(Character).filter(Character.search_character_id == character.id).update({
        "search_character_id": 1,
    })
    g.db.query(SearchCharacterChoice).filter(SearchCharacterChoice.search_character_id == id).delete()
    # Don't use g.db.delete(character) because it does a load of extra queries
    # for foreign keys and stuff.
    g.db.query(SearchCharacter).filter(SearchCharacter.id == id).delete()
    return redirect(url_for("rp_search_character_list"))

