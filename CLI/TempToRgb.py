class TempToRgb():
    def __init__(self, _temp = None):
        self.temp = _temp

    def get_regression(self, fit, x):
        regression = fit[0] * (pow(x, 2)) + fit[1] * (x) + fit[2]
        return int(regression)

    def check_RGB(self, rgb):
        rgb_range_upper = 255
        rgb_range_lower = 0
        #check to make sure RGB values are between 0, 255
        for color in range(0,3):
            if(rgb[color] > rgb_range_upper):
                rgb[color] = rgb_range_upper
            if(rgb[color] < rgb_range_lower):
                rgb[color] = rgb_range_lower
        return rgb

    def get_rgb(self):
        #Temp will get the
        #Fit variables are coefficients for the regression model
        #Regression calculations found in MATLAB file
        fit = [None] * 3
        rgb = [None] * 3
        #regression coefficients
        fit[0] = [0.1504, -16.8053, 509.9143]
        fit[1] = [-0.1473, 19.2913, -410.0381]
        fit[2] = [-0.0042, -3.7102, 368.9524]
        for color in range(0, 3):
            rgb[color] = self.get_regression(fit[color], self.temp)

        rgb = self.check_RGB(rgb)
        return rgb    
