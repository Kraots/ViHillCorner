from disnake import Colour


class Colours:
    """
    Available colours:
    ------------------

        - `invisible`
        - `red`
        - `orange`
        - `pastel`
        - `yellow`
        - `light_pink`
        - `blue`
        - `reds`
        - `light_blue`
    """

    def __init__(self) -> None:
        pass

    @property
    def invisible(self) -> Colour:
        return Colour(0x2F3136)

    @property
    def red(self) -> Colour:
        return Colour(0xe64343)

    @property
    def orange(self) -> Colour:
        return Colour(0xe97115)

    @property
    def pastel(self) -> Colour:
        return Colour(0xc69eff)

    @property
    def yellow(self) -> Colour:
        return Colour(0xb9b211)

    @property
    def light_pink(self) -> Colour:
        return Colour(0xf1a3d8)

    @property
    def blue(self) -> Colour:
        return Colour(0x708DD0)

    @property
    def reds(self) -> Colour:
        return Colour(0xf93b3b)

    @property
    def light_blue(self) -> Colour:
        return Colour(0x94feff)


Colours = Colours()
Colors = Colours
