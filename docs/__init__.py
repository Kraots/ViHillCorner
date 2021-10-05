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
    from ._cog import DocCog
    bot.add_cog(DocCog(bot))
    # There's a chance that it won't add the cog for whatever reason
    # so it's recommended you also add it in on_ready
    # Example:

    """in your on_ready:
    try:
        bot.load_extension('cogs')
    except Exception:
        pass
    """
