from math import ceil

def pagination(form, page, limit) :
    return {"current_page": page, "limit": limit, "pages": ceil(form.count() / limit), "data": form.offset((page - 1) * limit).limit(limit).all()}