from flask import Blueprint
from services.seo_description_generator import handle_generate_seo_descriptions

seo_blueprint = Blueprint("seo", __name__)

@seo_blueprint.route("/generate-seo-descriptions", methods=["POST"])
def generate_seo_descriptions():
    return handle_generate_seo_descriptions()
