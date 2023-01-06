"""Helper utilities and decorators."""


def make_dropdown(model, field) -> list[tuple]:
    """Returns the elements for a drop down"""
    return [(g.id, g.field) for g in model.query.all()]
