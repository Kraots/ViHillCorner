try:
    from bot import ViHillCorner
except Exception:
    from main import ViHillCorner

MAX_SIGNATURE_AMOUNT = 3
PRIORITY_PACKAGES = (
    "python",
)
NAMESPACE = "doc"


def setup(bot: ViHillCorner) -> None:
    """Load the Doc cog."""
    from .cog import Docs
    bot.add_cog(Docs(bot))
