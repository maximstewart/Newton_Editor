# Python imports
import colorsys

# Lib imports

# Application imports


class ColorConverterMixin:
    # NOTE: HSV HSL, and Hex Alpha parsing are available in Gtk 4.0- not lower.
    #       So, for compatability we're gunna convert to rgba string ourselves...
    def get_color_text(self, buffer, start, end):
        text = buffer.get_text(start, end, include_hidden_chars = False)

        try:
            if "hsl" in text:
                text = self.hsl_to_rgb(text)

            if "hsv" in text:
                text = self.hsv_to_rgb(text)

            if "#" == text[0]:
                hex  = text[1:]
                size = len(hex)
                if size in [4, 8, 16]:
                    rgba = self.hex_to_rgba(hex, size)
                    print(rgba)

        except Exception as e:
            ...

        return text

    def hex_to_rgba(self, hex, size):
        rgba  = []
        slots = None
        step  = 2
        bytes = 16

        if size == 4:              # NOTE: RGBA
            step  = 1
            slots = (0, 1, 2, 3)

        if size == 6:              # NOTE: RR GG BB
            slots = (0, 2, 4)

        if size == 8:              # NOTE: RR GG BB AA
            step  = 2
            slots = (0, 2, 4, 6)

        if size == 16:              # NOTE: RRRR GGGG BBBB AAAA
            step  = 4
            slots = (0, 4, 8, 12)

        for i in slots:
            v = int(hex[i : i + step], bytes)
            rgba.append(v)


        rgb_sub = ','.join(map(str, tuple(rgba)))

        return f"rgba({rgb_sub})"

        # return tuple(rgba)



    def hsl_to_rgb(self, text):
        _h, _s , _l = text.replace("hsl", "") \
                        .replace("deg", "") \
                        .replace("(", "") \
                        .replace(")", "") \
                        .replace("%", "") \
                        .replace(" ", "") \
                        .split(",")

        h = None
        s = None
        l = None

        h, s , l = int(_h) / 360, float(_s) / 100, float(_l) / 100

        rgb  = tuple(round(i * 255) for i in colorsys.hls_to_rgb(h, l, s))
        rgb_sub = ','.join(map(str, rgb))

        return f"rgb({rgb_sub})"


    def hsv_to_rgb(self, text):
        _h, _s , _v = text.replace("hsv", "") \
                        .replace("deg", "") \
                        .replace("(", "") \
                        .replace(")", "") \
                        .replace("%", "") \
                        .replace(" ", "") \
                        .split(",")

        h = None
        s = None
        v = None

        h, s , v = int(_h) / 360, float(_s) / 100, float(_v) / 100

        rgb  = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
        rgb_sub = ','.join(map(str, rgb))

        return f"rgb({rgb_sub})"
