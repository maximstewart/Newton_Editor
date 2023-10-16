# Python imports
import colorsys

# Lib imports

# Application imports


class ColorConverterMixin:
    def get_color_text(self, buffer, start, end):
        text  = buffer.get_text(start, end, include_hidden_chars = False)

        try:
            if "hsl" in text:
                text = self.hsl_to_rgb(text)

            if "hsv" in text:
                text = self.hsv_to_rgb(text)
        except Exception as e:
            ...

        return text

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
