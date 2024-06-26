import gettext
import os

lang_code = globals().get("LANG") or os.getenv("LANG") or "en"
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "translations")
lang = gettext.translation("geopic_tag_reader", localedir, languages=[lang_code], fallback=True)
lang.install()
_ = lang.gettext
