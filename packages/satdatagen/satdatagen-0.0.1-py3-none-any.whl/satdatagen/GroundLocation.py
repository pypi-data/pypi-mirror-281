from astropy.coordinates import EarthLocation
from astropy import units as u
import openmeteo_requests
from datetime import datetime
from TimeRange import TimeRange
		
class GroundLocation:
	def __init__(self, lat, lon, time_range):
		self.lon = lon
		self.lat = lat
		self.el = EarthLocation(lat = lat*u.deg, lon = lon*u.deg)
		self.time_range = time_range

		self.cloud_prob = self._get_cloud_cover()

	def set_latlon(self, lat, lon):
		self.lat = lat
		self.lon = lon

	def get_latlon(self):
		return lat,lon

	def EarthLocation(self):
		return self.el

	def set_time_range(self, time_range):
		self.time_range = time_range

	def get_time_range(self):
		return self.time_range

	def __str__(self):
		return f'Latitude: {self.lat}, Longitude: {self.lon}, Time range: {self.time_range}'

	def _get_cloud_cover(self):
		openmeteo = openmeteo_requests.Client()
		# Make sure all required weather variables are listed here
		# The order of variables in hourly or daily is important to assign them correctly below
		url = "https://archive-api.open-meteo.com/v1/archive"
		params = {
			"latitude": self.lat,
			"longitude": self.lon,
			"start_date": f'{self.time_range.start.to_value("iso", subfmt="date")}',
			"end_date": f'{self.time_range.end.to_value("iso", subfmt="date")}',
			"hourly": ["cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
			"timezone": "auto"
		}
		responses = openmeteo.weather_api(url, params=params)

		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		# print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
		# print(f"Elevation {response.Elevation()} m asl")
		# print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
		# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

		# Process hourly data. The order of variables needs to be the same as requested.
		hourly = response.Hourly()
		hourly_cloud_cover = hourly.Variables(0).ValuesAsNumpy()
		hourly_cloud_cover_low = hourly.Variables(1).ValuesAsNumpy()
		hourly_cloud_cover_mid = hourly.Variables(2).ValuesAsNumpy()
		hourly_cloud_cover_high = hourly.Variables(3).ValuesAsNumpy()
		return hourly_cloud_cover


if __name__ == '__main__':
	lat = 48.78 #degrees north
	lon = 9.18 #degrees west

	temp = datetime(2024, 6, 10, hour=14, minute=30)
	time_range = TimeRange(temp, periods = 5, delta = 500)

	haystack = GroundLocation(lat, lon, time_range = time_range)
	clouds = haystack.cloud_prob
	print(clouds)