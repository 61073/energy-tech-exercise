import json
import os

from src.app.weather_data_receiver import get_weather_degree_days


class DataCalculator:

    def __init__(self, house_data):
        self.heating_factor = None
        self.insulation_factor = None
        self.floor_area = None
        self.id = None
        self.location = None
        self._initialise_variables(house_data)

    def _initialise_variables(self, house_data):
        """
        Initialises class variables for the DataCalculator class from the given house_data details provided

        Params:
            house_data(dict): house data provided with all calculation values required
        """
        self.heating_factor = house_data.get("heatingFactor")
        self.insulation_factor = house_data.get("insulationFactor")
        self.floor_area = house_data.get("floorArea")
        self.id = house_data.get("submissionId")
        self.location = house_data.get("designRegion")

    def process_results(self):
        """
        Uses class variables and static methods in this file, along with the weather data receiver API response to give
         the formatted string with all the calculated values.

        Returns:
             results(str): formatted string with all relevant data and calculated values
        """
        heat_loss = calculate_heat_loss(self.floor_area, self.heating_factor, self.insulation_factor)
        try:
            degree_days = get_weather_degree_days(self.location)
            power_heat_loss = calculate_power_heat_loss(heat_loss, degree_days)
            best_heat_pump_data = get_heat_pump_data(power_heat_loss)
            best_heat_pump_name = best_heat_pump_data.get("label")
            costs = best_heat_pump_data.get("costs")
            cost_breakdown_string = ""
            total_cost_ex_vat = 0
            for cost_dict in costs:
                label = cost_dict.get("label")
                cost = cost_dict.get("cost")
                cost_string = "%.2f" % cost
                cost_breakdown_string += f" {label}, {cost_string}\n"
                total_cost_ex_vat += cost
            total_cost_inc_vat = total_cost_ex_vat * 1.05
            total_cost_inc_vat_string = "%.2f" % total_cost_inc_vat
            results = f"--------------------------------------\n{self.id}\n" \
                      f"--------------------------------------\nEstimated Heat Loss = {round(heat_loss)}\nDesign" \
                      f" Region = {self.location}\nPower Heat Loss = {round(power_heat_loss)}\nRecommended Heat Pump " \
                      f"= {best_heat_pump_name}\nCost Breakdown:\n{cost_breakdown_string}Total Cost, including VAT = " \
                      f"{total_cost_inc_vat_string}"
            return results
        except Exception as e:
            # TODO - change this to a specific custom exception for weather data location not found
            error_results = f"--------------------------------------\n{self.id}\n" \
                            f"--------------------------------------\nHeating Loss: {round(heat_loss)}\n" \
                            f"Warning: Could not find design region"
            return error_results


def calculate_heat_loss(floor_area, heating_factor, insulation_factor):
    """
    Multiplies the values of area, heating and insulation factors to give kWh value of heat loss

    Params:
        floor_area(float): floor area in the specified customer house
        heating_factor(float): heating factor value for house
        insulation_factor(float): insulation factor value for house

    Returns:
        heat_loss(float): multiplied values of area, heating and insulation factors to give kWh value.
    """
    return floor_area * heating_factor * insulation_factor


def calculate_power_heat_loss(heat_loss, degree_days):
    """
    Divides the calculated heat loss value in kWh by the degree days to give power heat loss in kW.

    Params:
        heat_loss(float): calculated heat loss value in kWh
        degree_days(float): degree days values given from location and weather data

    Returns:
        power_heat_loss(float): divided value of heat loss and degree days
    """
    return heat_loss / degree_days


def get_heat_pump_data(power_heat_loss):
    """
    Uses power heat loss value in kW to return details of the closest pump that has greater power than the power heat
     loss value

    Params:
        power_heat_loss(float): calculated from calculate_power_heat_loss method

    Returns:
        best_pump(dict): all pump details for the most relevant pump power required
    """
    # TODO - clean this up and simplify
    pump_data_location = os.path.join("src", "app", "data", "heat-pumps.json")
    with open(pump_data_location) as pump_file:
        pump_data = json.load(pump_file)
        pump_file.close()
    pump_powers = []
    for pump in pump_data:
        power = pump.get("outputCapacity")
        pump_powers.append(power)
    pump_powers.sort()
    best_pump_num = None
    best_pump = None
    for pump_power in pump_powers:
        if power_heat_loss <= pump_power:
            best_pump_num = pump_power
            break
    for pump in pump_data:
        power = pump.get("outputCapacity")
        if power == best_pump_num:
            best_pump = pump
    return best_pump
