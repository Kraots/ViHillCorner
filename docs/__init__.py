from main import ViHillCorner
from .cache import DocCache

MAX_SIGNATURE_AMOUNT = 3
PRIORITY_PACKAGES = (
    "python",
)
NAMESPACE = "doc"
doc_cache = DocCache()


def setup(bot: ViHillCorner) -> None:
    """Load the Doc cog."""
    from .cog import Docs
    bot.add_cog(Docs(bot))
